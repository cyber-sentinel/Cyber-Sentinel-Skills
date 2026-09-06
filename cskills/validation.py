# Copyright (c) 2026 Ali RahimDabagh
# SPDX-License-Identifier: Apache-2.0

"""Strict data loading and offline contract validation. Never log payloads."""

import json
import math
import re
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry
from referencing.exceptions import NoSuchResource

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 262144
MAX_DEPTH = 32
SEMVER = r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
# '$' alone also matches before a terminal newline. Use a portable ECMAScript
# negative lookahead to enforce absolute end in the JSON Schema pattern.
SEMVER += r"(?![\s\S])"


class Rejected(ValueError):
    """An error code safe to return without revealing the rejected input."""


def deny(code):
    raise Rejected(code)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            deny("duplicate-json-key")
        result[key] = value
    return result


def _depth(value, level=0):
    if level > MAX_DEPTH:
        deny("nesting-limit")
    if isinstance(value, float) and not math.isfinite(value):
        deny("nonfinite-number")
    if isinstance(value, dict):
        for item in value.values():
            _depth(item, level + 1)
    elif isinstance(value, list):
        for item in value:
            _depth(item, level + 1)


def decode_json(data):
    if len(data) > MAX_BYTES:
        deny("byte-limit")
    try:
        result = json.loads(data, object_pairs_hook=_pairs,
                            parse_constant=lambda _: deny("nonfinite-number"))
    except (ValueError, UnicodeError, RecursionError) as exc:
        if isinstance(exc, Rejected):
            raise
        deny("invalid-json")
    _depth(result)
    return result


def bounded_path(root, relative):
    """Reject traversal, alternate separators and symlinks, including ancestors.

    Root is selected by the trusted caller. It must not be writable by an
    adversary during an operation: this is not a concurrent filesystem sandbox.
    """
    if not isinstance(relative, str) or not relative or "\\" in relative:
        deny("invalid-path")
    parts = relative.split("/")
    if any(p in ("", ".", "..") or ":" in p for p in parts):
        deny("invalid-path")
    if PurePosixPath(relative).is_absolute():
        deny("invalid-path")
    root = Path(root).absolute()
    for parent in (root, *root.parents):
        if parent.is_symlink() or getattr(parent, "is_junction", lambda: False)():
            deny("symlink-path")
    current = root
    for part in parts:
        current = current / part
        if current.is_symlink() or getattr(current, "is_junction", lambda: False)():
            deny("symlink-path")
    try:
        in_scope = current.resolve().is_relative_to(root.resolve())
    except (OSError, RuntimeError):
        deny("unresolvable-path")
    if not in_scope:
        deny("path-outside-scope")
    return current


def read_bytes(root, relative):
    path = bounded_path(root, relative)
    if not path.is_file():
        deny("missing-or-nonregular-file")
    try:
        with path.open("rb") as stream:
            data = stream.read(MAX_BYTES + 1)
    except OSError:
        deny("file-read-failed")
    if len(data) > MAX_BYTES:
        deny("byte-limit")
    return data


def read_json(root, relative):
    return decode_json(read_bytes(root, relative))


def canonical(value):
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, UnicodeError, RecursionError):
        deny("non-json-value")


def _no_retrieval(uri):
    raise NoSuchResource(ref=uri)


def check_schema(schema):
    """Only local fragment references. No network or filesystem resolution."""
    def visit(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in ("$ref", "$dynamicRef") and (
                    not isinstance(item, str) or not item.startswith("#/")
                ):
                    deny("nonlocal-schema-reference")
                visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)
    visit(schema)
    try:
        Draft202012Validator.check_schema(schema)
    except Exception:
        deny("invalid-schema")


def validate_data(value, schema):
    check_schema(schema)
    try:
        errors = Draft202012Validator(
            schema, registry=Registry(retrieve=_no_retrieval),
            format_checker=FormatChecker(),
        ).iter_errors(value)
        if next(errors, None) is not None:
            deny("schema-rejected")
    except Rejected:
        raise
    except Exception:
        deny("schema-evaluation-failed")


SENSITIVE_FIELDS = re.compile(
    r"^(?:password|passwd|pwd|api[-_]?key|access[-_]?token|refresh[-_]?token|"
    r"token|secret|client[-_]?secret|private[-_]?key|credentials?|authorization)$",
    re.I,
)
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{12,}", re.I),
    re.compile(r"(?i)\b(?:password|passwd|api_key|api-key|access_token|client_secret)\s*[:=]\s*[\"']?[^\s\"',;]{4,}"),
    re.compile(r"(?i)https?://[^\s/@:]+:[^\s/@]+@"),
]


def check_secret_surface(value):
    """Conservative heuristic, not a guarantee that arbitrary secrets are absent."""
    if isinstance(value, dict):
        for key, item in value.items():
            if SENSITIVE_FIELDS.fullmatch(str(key)):
                deny("secret-like-field")
            check_secret_surface(item)
    elif isinstance(value, list):
        for item in value:
            check_secret_surface(item)
    elif isinstance(value, str):
        if any(p.search(value) for p in SECRET_PATTERNS):
            deny("secret-like-value")


def parse_frontmatter(text):
    # Foundation uses a deliberately small YAML profile: two JSON-quoted scalars.
    # A restricted parser prevents aliases, custom tags, duplicate keys and drift.
    lines = text.splitlines()
    if len(lines) < 5 or lines[0] != "---" or lines[3] != "---":
        deny("frontmatter-profile")
    meta = {}
    for line in lines[1:3]:
        key, sep, raw = line.partition(": ")
        if not sep or key in meta or key not in ("name", "description"):
            deny("frontmatter-profile")
        try:
            meta[key] = json.loads(raw)
        except ValueError:
            deny("frontmatter-profile")
        if not isinstance(meta[key], str):
            deny("frontmatter-profile")
    if set(meta) != {"name", "description"}:
        deny("frontmatter-profile")
    return meta


def load_manifest(root, relative):
    folder = bounded_path(root, relative)
    manifest = read_json(folder, "skill.json")
    validate_data(manifest, read_json(root, "schemas/skill-contract.schema.json"))
    check_secret_surface(manifest)
    meta = parse_frontmatter(read_bytes(folder, "SKILL.md").decode("utf-8"))
    if meta != {k: manifest[k] for k in ("name", "description")}:
        deny("frontmatter-manifest-mismatch")
    if folder.name != manifest["name"] or folder.parent.name != manifest["category"]:
        deny("skill-directory-mismatch")
    return manifest, folder


def manifests(root=ROOT):
    result = []
    for path in sorted((Path(root) / "skills").glob("*/*/skill.json")):
        relative = path.parent.relative_to(root).as_posix()
        result.append(load_manifest(root, relative))
    if not result:
        deny("empty-catalog")
    ids = [item[0]["id"] for item in result]
    if len(ids) != len(set(ids)):
        deny("duplicate-skill-id")
    return result
