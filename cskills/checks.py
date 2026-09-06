# Copyright (c) 2026 Ali RahimDabagh
# SPDX-License-Identifier: Apache-2.0

"""Repository gates. These checks complement review; they do not sandbox code."""

import ast
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

from .handlers import HANDLERS
from .licensing import check_license_materials
from .runtime import authorize, run
from .validation import (ROOT, bounded_path, check_schema, check_secret_surface,
                         deny, manifests, read_bytes, read_json)

IGNORE = {".git", ".venv", "__pycache__", ".pytest_cache", "dist", ".coverage"}
SENSITIVE_NAMES = {".env", ".netrc", ".npmrc", "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519", "credentials", "credentials.json"}
SENSITIVE_SUFFIXES = {".key", ".pem", ".pfx", ".p12", ".jks", ".kdbx"}


def inventory(root=ROOT):
    """Inventory source without following symlinks or ignored build directories."""
    root = Path(root)
    def visit(folder):
        for path in sorted(folder.iterdir()):
            if path.is_symlink():
                deny("repository-symlink")
            if path.name in IGNORE:
                continue
            relative = path.relative_to(root).as_posix()
            bounded_path(root, relative)
            if path.is_dir():
                yield from visit(path)
            elif path.is_file():
                yield relative
            else:
                deny("repository-nonregular-file")
    return list(visit(root))


def check_links(root, files):
    # Offline gate: relative file targets and URL schemes. It does not claim
    # external reachability or validate heading anchors (documented separately).
    for relative in files:
        if not relative.endswith(".md"):
            continue
        text = read_bytes(root, relative).decode("utf-8")
        for target in re.findall(r"!?\[[^\]\n]*\]\(([^\s)]+)\)", text):
            if target.startswith("#"):
                continue
            url = urlsplit(target)
            if url.scheme:
                if url.scheme not in ("https", "mailto"):
                    deny("unsafe-documentation-link")
                continue
            if target.startswith("//") or "\\" in target:
                deny("unsafe-documentation-link")
            path = (Path(root) / relative).parent / unquote(url.path)
            resolved = path.resolve()
            if not resolved.is_relative_to(Path(root).resolve()) or not resolved.exists():
                deny("broken-documentation-link")


def check_handler_surface(root):
    parsed = ast.parse(read_bytes(root, "cskills/handlers.py"))
    allowed_imports = {"hashlib", "ipaddress", "re", "datetime", "validation"}
    forbidden_calls = {"open", "eval", "exec", "compile", "__import__", "getattr",
                       "setattr", "delattr", "globals", "locals", "vars", "input", "breakpoint"}
    for node in ast.walk(parsed):
        if isinstance(node, ast.Import):
            if any(alias.name not in allowed_imports for alias in node.names):
                deny("undeclared-handler-import")
        if isinstance(node, ast.ImportFrom):
            if node.module not in allowed_imports or any(a.name == "*" for a in node.names):
                deny("undeclared-handler-import")
        if isinstance(node, ast.Name) and (node.id in forbidden_calls or node.id.startswith("__")):
            deny("unsafe-handler-primitive")
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            deny("unsafe-handler-primitive")


def check_workflows(root, files):
    for relative in files:
        if not relative.startswith(".github/workflows/"):
            continue
        content = read_bytes(root, relative).decode("utf-8")
        workflow = yaml.safe_load(content)
        if not isinstance(workflow, dict):
            deny("invalid-workflow")
        triggers = workflow.get("on", workflow.get(True))  # YAML 1.1 'on' scalar
        if not isinstance(triggers, dict) or set(triggers) != {"push", "pull_request"}:
            deny("unsupported-workflow-trigger")
        if workflow.get("permissions") != {"contents": "read"}:
            deny("unsafe-workflow-permissions")
        for action in re.findall(r"uses:\s*([^\s]+)", content):
            if not re.fullmatch(r"actions/(?:checkout|setup-python)@[0-9a-f]{40}", action):
                deny("unpinned-or-unapproved-action")
        for job in workflow.get("jobs", {}).values():
            if "permissions" in job or "secrets" in job:
                deny("workflow-privilege-override")
            for step in job.get("steps", []):
                if step.get("uses", "").startswith("actions/checkout@"):
                    if step.get("with", {}).get("persist-credentials") is not False:
                        deny("persisted-checkout-credentials")


def validate_repository(root=ROOT):
    root = Path(root)
    files = inventory(root)
    if not {"LICENSE", "NOTICE"}.issubset(files):
        deny("missing-license-materials")
    check_license_materials(read_bytes(root, "LICENSE"), read_bytes(root, "NOTICE"))
    for relative in files:
        path = Path(relative)
        if relative == "BUNDLE-MANIFEST.json":
            deny("reserved-bundle-filename")
        if (path.name.lower() in SENSITIVE_NAMES or path.name.lower().startswith(".env.")
                or path.suffix.lower() in SENSITIVE_SUFFIXES):
            deny("sensitive-filename")
        content = read_bytes(root, relative)
        try:
            text = content.decode("utf-8")
        except UnicodeError:
            deny("unexpected-binary-source")
        check_secret_surface(text)
    catalog = manifests(root)
    if {m["id"] for m, _ in catalog} != set(HANDLERS):
        deny("catalog-registry-mismatch")
    declared_skill_files = set()
    for manifest, folder in catalog:
        authorize(manifest)
        relative = folder.relative_to(root).as_posix()
        allowed = {"SKILL.md", "skill.json", "input.schema.json", "output.schema.json"}
        for example in manifest["examples"]:
            allowed.update(example.values())
            data = read_json(folder, example["input"])
            expected = read_json(folder, example["expected"])
            actual = run(manifest["id"], data, root)["result"]
            if actual != expected:
                deny("fixture-result-mismatch")
        declared_skill_files.update(f"{relative}/{p}" for p in allowed)
        for filename in ("input.schema.json", "output.schema.json"):
            check_schema(read_json(folder, filename))
        for test in manifest["tests"]:
            if not bounded_path(root, test).is_file() or not test.startswith("tests/test_"):
                deny("missing-declared-test")
    if {p for p in files if p.startswith("skills/")} != declared_skill_files:
        deny("undeclared-or-missing-skill-file")
    for relative in files:
        if relative.endswith(".json"):
            check_secret_surface(read_json(root, relative))
    check_handler_surface(root)
    check_links(root, files)
    check_workflows(root, files)
    return {"skills": len(catalog), "source_files": len(files), "status": "passed"}
