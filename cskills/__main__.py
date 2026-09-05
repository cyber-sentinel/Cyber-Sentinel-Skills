"""Host CLI: explicit bounded input, result-only stdout, payload-free errors."""

import argparse
import json
import sys
from pathlib import Path

from .checks import validate_repository
from .packaging import build_bundle
from .runtime import run
from .validation import Rejected, canonical, deny, read_json


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m cskills")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="Validate catalog, fixtures, links, policy and packaging inputs")
    commands.add_parser("release-check", help="Report the open owner license decision; does not release")
    execute = commands.add_parser("run", help="Run a registered offline handler")
    execute.add_argument("skill_id")
    execute.add_argument("--workspace", required=True, type=Path)
    execute.add_argument("--input", required=True, help="Relative JSON file within the workspace")
    package = commands.add_parser("package", help="Create an original-source review ZIP; no publishing")
    package.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            result = validate_repository()
        elif args.command == "release-check":
            deny("license-owner-approval-pending")
        elif args.command == "run":
            result = run(args.skill_id, read_json(args.workspace, args.input))
        else:
            output = args.output.absolute()
            if output.suffix != ".zip" or not output.parent.is_dir():
                deny("invalid-bundle-output")
            if any(p.is_symlink() or getattr(p, "is_junction", lambda: False)()
                   for p in (output, *output.parents)):
                deny("symlink-path")
            data = build_bundle()
            # Exclusive creation: never overwrite source, evidence or an old bundle.
            with output.open("xb") as stream:
                stream.write(data)
            result = {"status": "created", "purpose": "review-only", "bytes": len(data)}
        sys.stdout.buffer.write(canonical(result) + b"\n")
        return 0
    except (Rejected, OSError, UnicodeError) as exc:
        code = str(exc) if isinstance(exc, Rejected) else "host-io-failed"
        sys.stderr.write(json.dumps({"error": code}) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
