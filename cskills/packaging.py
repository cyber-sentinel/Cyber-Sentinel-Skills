"""Deterministic review bundles. No extraction or public release operation."""

import hashlib
import io
import zipfile

from .checks import inventory, validate_repository
from .validation import (MAX_BYTES, ROOT, canonical, decode_json, deny,
                         read_bytes)

MAX_BUNDLE_BYTES = 5 * 1024 * 1024
MAX_FILES = 512


def build_bundle(root=ROOT):
    validate_repository(root)
    files = {p: read_bytes(root, p) for p in inventory(root)}
    if len(files) > MAX_FILES or sum(map(len, files.values())) > MAX_BUNDLE_BYTES:
        deny("bundle-limit")
    manifest = {
        "format_version": "0.1.0", "purpose": "review-only",
        "license_status": "pending-owner-approval",
        "files": {p: hashlib.sha256(content).hexdigest() for p, content in sorted(files.items())},
    }
    files["BUNDLE-MANIFEST.json"] = canonical(manifest) + b"\n"
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as bundle:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, content)
    data = output.getvalue()
    verify_bundle(data)
    return data


def verify_bundle(data):
    if len(data) > MAX_BUNDLE_BYTES:
        deny("bundle-limit")
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as bundle:
            entries = bundle.infolist()
            names = [item.filename for item in entries]
            if len(names) > MAX_FILES + 1 or len(set(names)) != len(names):
                deny("bundle-duplicate-or-excess-members")
            if sum(item.file_size for item in entries) > MAX_BUNDLE_BYTES:
                deny("bundle-limit")
            for item in entries:
                name = item.filename
                if (any(p in ("", ".", "..") for p in name.split("/"))
                        or "\\" in name or ":" in name or name.startswith("/")
                        or item.is_dir() or item.file_size > MAX_BYTES
                        or item.compress_type != zipfile.ZIP_STORED
                        or (item.external_attr >> 16) != 0o100644):
                    deny("unsafe-bundle-member")
            manifest = decode_json(bundle.read("BUNDLE-MANIFEST.json"))
            if (set(manifest) != {"format_version", "purpose", "license_status", "files"}
                    or manifest["format_version"] != "0.1.0"
                    or manifest["purpose"] != "review-only"
                    or manifest["license_status"] != "pending-owner-approval"
                    or not isinstance(manifest["files"], dict)):
                deny("invalid-bundle-manifest")
            expected = set(manifest["files"]) | {"BUNDLE-MANIFEST.json"}
            if set(names) != expected:
                deny("bundle-members-mismatch")
            for name, digest in manifest["files"].items():
                if hashlib.sha256(bundle.read(name)).hexdigest() != digest:
                    deny("bundle-digest-mismatch")
            return {"status": "passed", "files": len(manifest["files"]),
                    "sha256": hashlib.sha256(data).hexdigest()}
    except (zipfile.BadZipFile, KeyError, TypeError, AttributeError):
        deny("invalid-bundle")
