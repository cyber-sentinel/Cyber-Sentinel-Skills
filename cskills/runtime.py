# Copyright (c) 2026 Ali RahimDabagh
# SPDX-License-Identifier: Apache-2.0

"""A fixed offline execution profile, not a sandbox for untrusted Python."""

import hashlib
from copy import deepcopy

from .handlers import HANDLERS
from .validation import (MAX_BYTES, ROOT, canonical, check_secret_surface,
                         decode_json, deny, manifests, read_json, validate_data)


def authorize(manifest):
    """Policy is code owned by the host, never a grant inside an LLM response.

    Foundation has no mechanism to authorize external effects. Such proposals
    fail closed, even when their manifest claims user approval.
    """
    registered = HANDLERS.get(manifest["id"])
    if not registered or (manifest["category"], manifest["name"]) != registered[:2]:
        deny("unregistered-handler")
    expected = {
        "capabilities": ["READ", "ANALYZE", "GENERATE"],
        "network": {"enabled": False, "hosts": []},
        "filesystem": {"read": [], "write": []},
        "shell": False, "privilege_escalation": False,
        "environment": [], "external_services": [],
    }
    if manifest["permissions"] != expected:
        deny("unsupported-permission-profile")
    if manifest["side_effects"] or manifest["required_tools"] or manifest["dependencies"]:
        deny("unsupported-external-dependency-or-effect")
    if manifest["safety"] != {
        "classification": "passive-analysis", "destructive": False,
        "authorization_policy": "none-no-side-effects", "secret_handling": "reject",
    }:
        deny("unsupported-safety-profile")
    if manifest["execution"] != {
        "kind": "builtin", "entrypoint": manifest["id"],
        "determinism": "deterministic", "ai": {"required": False, "providers": []},
        "source_content_execution": False,
    }:
        deny("unsupported-execution-profile")
    return registered[2]


def run(skill_id, data, root=ROOT):
    catalog = manifests(root)
    match = next(((m, p) for m, p in catalog if m["id"] == skill_id), None)
    if match is None:
        deny("unknown-skill")
    manifest, folder = match
    handler = authorize(manifest)
    # Re-encode to bound and detach the caller's mutable payload; no grants read.
    raw = canonical(data)
    data = decode_json(raw)
    check_secret_surface(data)
    validate_data(data, read_json(folder, manifest["inputs"]["schema"]))
    result = handler(deepcopy(data))
    check_secret_surface(result)
    validate_data(result, read_json(folder, manifest["outputs"]["schema"]))
    envelope = {
        "contract_version": manifest["contract_version"],
        "skill_id": manifest["id"], "skill_version": manifest["version"],
        "determinism": "deterministic", "input_sha256": hashlib.sha256(raw).hexdigest(),
        "sources": sorted(data["sources"], key=lambda s: s["id"]),
        "result": result,
    }
    if len(canonical(envelope)) > MAX_BYTES:
        deny("output-byte-limit")
    validate_data(envelope, read_json(root, "schemas/result-envelope.schema.json"))
    return envelope
