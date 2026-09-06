# ADR-0001: Foundation architecture

Status: implemented proposal for owner review. Contract version: `0.1.0`.

## Context and decision

The approved milestone is a governed capability layer with 3–5 validated
exemplars, independent of Atlas. A generic prompt catalog would not enforce the
required permissions. A general shell/plugin orchestrator would expand the trust
boundary before safe execution adapters have been designed.

Use JSON Schema Draft 2020-12 for a versioned `skill.json` execution contract,
standard `SKILL.md` discovery instructions, and a small Python 3.11+ host with
four registered pure handlers. No handler code is loaded from a manifest path.
The machine-readable contract is canonical for execution; the Markdown name and
description must agree with it. The restricted two-scalar frontmatter profile is
valid YAML and deliberately excludes aliases, executable tags and duplicate keys.
See the [Agent Skills format](https://agentskills.io/specification) and
[JSON Schema specification](https://json-schema.org/draft/2020-12).

## Components

| Component | Responsibility |
|---|---|
| `skills/<family>/<name>/` | Instructions, contract, input/output schemas and example pair |
| `schemas/` | Versioned contract and result envelope |
| `cskills/validation.py` | Strict JSON, bounded paths, schema and secret-surface checks |
| `cskills/runtime.py` | Host policy decision, fixed dispatch and input/output validation |
| `cskills/handlers.py` | Four reviewed in-memory transformations |
| `cskills/checks.py` | Repository, fixture, documentation and workflow gates |
| `cskills/packaging.py` | Reproducible review bundle and integrity verification |
| `tests/` | Synthetic behavioral, policy, CLI and packaging tests |
| `.github/workflows/ci.yml` | Cross-platform validation without write permissions or secrets |

The candidate `tools/validation/` and `tools/packaging/` directories are represented
by one importable package and one CLI. This avoids redundant wrappers and preserves
the ability to use handlers from a trusted embedding application. There are no
empty catalog families, generated prompt dumps, database, web UI or installer.

## Execution contract

The host validates manifest and input, applies a deterministic policy, calls the
fixed handler and validates its result. The envelope preserves sources, Skill
identity/version and a canonical input SHA-256. JSON key order does not affect
the digest; array order does. Canonical encoding is a documented project profile
(`json.dumps`, sorted keys, UTF-8, no NaN/Infinity), not a claim of RFC 8785 compliance.

Each result contains explicit limitations. Supplied fact/inference labels remain
supplied labels, not facts verified by this framework. No current handler depends
on AI. Future nondeterministic implementations must declare that fact, including
model dependency, and be evaluated separately from these deterministic handlers.

Policy accepts only the exact offline profile: `READ`, `ANALYZE`, `GENERATE`, no
filesystem/network/shell/environment/tool/service access, no side effects and no
source execution. Other capability classes exist in the contract vocabulary but
are unsupported by Foundation and rejected. There is no `--approve` escape hatch.

## Alternatives and consequences

| Alternative | Decision and consequence |
|---|---|
| Markdown-only skills | Rejected as the authoritative execution contract; permissions would be descriptive |
| YAML as the canonical manifest | JSON chosen for duplicate-key rejection, schema tooling and a narrower parser surface |
| General dynamic Python/shell plugin loader | Deferred; needs process isolation and mediated side effects |
| MCP-first runtime | Deferred; adapter interoperability must not define the product model |
| Vendor-specific agent SDK | Avoided in Foundation; optional adapters can wrap the same bounded contract later |

Python is a replaceable reference implementation, not a required format for
future consumer applications. Dependencies and actions are pinned, but pins do not
prove supply-chain safety. A future signed distribution and verified dependency
wheelhouse need separate release work. No dependencies are vendored in bundles.

The trust boundary assumes a reviewed, owner-controlled checkout. Modifying host
Python can modify policy; a manifest cannot prevent a malicious host. Filesystem
scope checks assume the selected root is not concurrently attacker-writable.
See the [threat model](../security/threat-model.md) for precise limitations.
