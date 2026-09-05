# Cyber Sentinel — Skills

Reusable cybersecurity capabilities for agents, with inspectable playbooks for
human analysts. Foundation v0.1 provides a versioned Skill contract, deterministic
offline handlers, validation gates and original exemplar Skills.

**Status: experimental foundation, under review. Project license: pending owner
approval. No public release or production deployment is included.**

## What is implemented

| Skill | Observable result | Deliberate limit |
|---|---|---|
| [Summarize evidence](skills/research/summarize-evidence/SKILL.md) | Ordered claims, sources, separate fact/inference counts | Does not verify the truth of supplied claims |
| [Normalize IOCs](skills/threat-intelligence/normalize-iocs/SKILL.md) | Deduplicated indicators with merged references and invalid-record results | No DNS, reputation lookup or enrichment |
| [Build timeline](skills/incident-response/build-timeline/SKILL.md) | Stable UTC ordering with original timestamps and source IDs | Requires known offsets; does not infer causality |
| [Review detection specification](skills/detection-engineering/review-detection-spec/SKILL.md) | Missing metadata findings with explicit query backend identity | Does not parse, execute or certify queries |

All four run without an LLM. Each consumes bounded JSON and produces validated
JSON. Their registered handlers have no network, shell, environment or filesystem
capabilities. The host CLI separately reads the explicitly selected input file.

## Try the synthetic examples

Use Python 3.11 or 3.12 in an isolated development environment. Run these commands
from the repository root; dependency installation needs package-index access.
After installation, validation and all exemplar execution work offline.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m cskills validate
python -m unittest discover -s tests -v
python -m cskills run cs.skills.threat-intelligence.normalize-iocs --workspace skills/threat-intelligence/normalize-iocs/examples --input input.json
```

An installation needs only the listed Python dependencies; no Atlas deployment,
MCP server, external security service, API credential or model account is needed.
The [example guide](examples/README.md) explains the other invocations and output
envelope. Errors contain stable codes, without echoing input values.

## Architecture and trust

[`skill.json`](skills/research/summarize-evidence/skill.json) is the canonical
execution contract. `SKILL.md` carries discovery and analyst/agent instructions.
The [architecture decision](docs/architecture/0001-foundation.md) explains the
fixed offline profile, Python implementation and future adapter boundary.

This is a host policy gate for reviewed built-in handlers, **not an OS sandbox
for arbitrary third-party Python**. A generic agent loading only `SKILL.md` does
not inherit this runtime's authorization guarantees. Network or mutating adapters
require a separate architecture review, trusted authorization and enforcement
outside the LLM. The [security model](docs/security/threat-model.md) describes
these boundaries, filesystem assumptions and remaining risks.

## Scope

This repository owns Skill definitions, packaging, contracts, validation, tests,
examples, security policy and documentation. It is independent of Atlas and
DefenseOps. Atlas owns its knowledge model, ingestion, provenance, search and
analyst workbench. DefenseOps owns detection content and Detection Forge IR.

Future Atlas context or API adapters may feed bounded evidence into Skills. Skill
output is not automatically authoritative Atlas knowledge. MCP is an optional
future interoperability adapter, not a canonical model or Foundation dependency.
See the [integration boundary](docs/architecture/integration.md).

## Review and contribution

- [Taxonomy and authoring contract](docs/skill-authoring/contract.md)
- [Engineering workflow](CONTRIBUTING.md)
- [Security reporting](SECURITY.md)
- [Reference and licensing research](docs/research/upstream-review.md)
- [Open decisions and repository governance](docs/governance/decisions.md)
- [License status](LICENSE_STATUS.md)
- [Changes](CHANGELOG.md)

Build a reproducible review bundle into an existing directory with a new filename:

```bash
python -m cskills package --output ../skills-foundation-review.zip
```

The bundle includes source, contracts, examples, tests, docs and a SHA-256 file
inventory. It excludes the Git database and build caches. Checksums detect changes;
they are not an authenticity signature. This command does not publish a release.
`python -m cskills release-check` intentionally returns exit code 2 while the
owner's license decision remains open.
