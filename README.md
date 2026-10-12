<h1 align="center">Cyber-Sentinel Skills</h1>
<p align="center"><strong>Governed Cybersecurity Operational Skills & Playbooks</strong></p>
<p align="center">APPLY • EXECUTE • REVIEW • REUSE • GOVERN</p>

<p align="center">
  <img alt="Foundation v0.1" src="https://img.shields.io/badge/Foundation%20v0.1-under%20review-blueviolet">
  <img alt="Offline Runtime" src="https://img.shields.io/badge/runtime-deterministic%20offline-0f766e">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11%20%7C%203.12-informational">
  <img alt="License" src="https://img.shields.io/badge/license-Apache--2.0-success">
  <img alt="Release" src="https://img.shields.io/badge/public%20release-not%20authorized-important">
</p>

Cyber-Sentinel Skills is the **APPLY** layer of the Cyber-Sentinel ecosystem. Foundation v0.1 turns analyst operating knowledge into bounded, inspectable execution contracts that can be used consistently by humans and, where appropriate, AI-assisted workflows.

> **Core question:** **How should this security task be performed consistently, safely, and verifiably?**

This Foundation is intentionally small and explicit: deterministic handlers, bounded JSON contracts, capability-aware host authorization, evidence-oriented outputs, and no hidden network or shell execution.

## Foundation Review State

| Boundary | State |
| --- | --- |
| Foundation v0.1 implementation | **Implemented on this review branch** |
| Deterministic offline handlers | **Implemented** |
| Skill contract + schemas | **Implemented** |
| Linux / Windows CI matrix | Python `3.11` / `3.12` |
| Apache-2.0 licensing | **Approved and present on this branch** |
| Official public release | **Not authorized** |
| Merge to `main` | **Blocked by remaining governance control** |
| Production certification | **Not claimed** |

A green Foundation check is engineering evidence. It does **not** bypass repository governance, owner release authority, environment-specific authorization, or production change control.

## Implemented Skills

| Skill | Observable result | Deliberate boundary |
| --- | --- | --- |
| [**Summarize evidence**](skills/research/summarize-evidence/SKILL.md) | ordered claims, sources, separate fact/inference counts | does not verify the truth of supplied claims |
| [**Normalize IOCs**](skills/threat-intelligence/normalize-iocs/SKILL.md) | deduplicated indicators, merged references, invalid-record results | no DNS, reputation lookup, or external enrichment |
| [**Build timeline**](skills/incident-response/build-timeline/SKILL.md) | stable UTC ordering with original timestamps and source IDs | requires known offsets; does not infer causality |
| [**Review detection specification**](skills/detection-engineering/review-detection-spec/SKILL.md) | missing-metadata findings with explicit query-backend identity | does not execute or certify detection queries |

All four Skills run **without an LLM**. Each consumes bounded JSON and produces validated JSON. Registered handlers have no declared network, shell, environment, external-service, destructive, or arbitrary filesystem capabilities.

## Skill Contract

A Skill is a **governed execution contract**, not a command list.

```text
Purpose
  ↓
Scope + Authorization
  ↓
Prerequisites + Inputs
  ↓
Bounded Procedure
  ↓
Decision Points
  ↓
Evidence + Verification
  ↓
Failure / Stop / Rollback
  ↓
Validated Outputs
  ↓
Attribution + Version History
```

The canonical machine-readable execution contract is `skill.json`. `SKILL.md` carries discovery and analyst/agent instructions. The host validates declared capabilities before invoking a reviewed built-in handler.

## Quick Start

Use Python 3.11 or 3.12 in an isolated development environment. Dependency installation requires package-index access; after installation, validation and exemplar execution work offline.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m cskills validate
python -m unittest discover -s tests -v
```

Run an exemplar:

```bash
python -m cskills run \
  cs.skills.threat-intelligence.normalize-iocs \
  --workspace skills/threat-intelligence/normalize-iocs/examples \
  --input input.json
```

No ATLAS deployment, MCP server, model account, API credential, or external security service is required for the Foundation runtime.

See [examples/README.md](examples/README.md) for the remaining invocations and result-envelope examples.

## Runtime & Trust Boundary

Foundation v0.1 is a **host policy gate for reviewed built-in handlers**. It is not an operating-system sandbox for arbitrary third-party Python.

The runtime enforces the declared Foundation profile around:

- bounded JSON input/output;
- schema validation;
- stable error codes;
- capability declarations;
- rejection of undeclared network, shell, environment, external-service, destructive, and filesystem effects;
- provenance and limitation envelopes;
- secret/error redaction expectations;
- deterministic fixtures and reproducible validation.

A generic agent loading only `SKILL.md` does **not** inherit these runtime authorization guarantees. Future mutating or networked adapters require separate architecture review, trusted authorization, and enforcement outside the LLM.

See:

- [Foundation Architecture](docs/architecture/0001-foundation.md)
- [Integration Boundary](docs/architecture/integration.md)
- [Threat Model](docs/security/threat-model.md)
- [Skill Authoring Contract](docs/skill-authoring/contract.md)

## Human + AI Operating Model

```text
Authorized Task
      ↓
Validated Skill Contract
      ↓
Human or AI-Assisted Execution
      ↓
Evidence Collection + Verification
      ↓
Review / Escalation / Rollback
      ↓
Recorded Outcome
```

AI assistance does not remove authorization, human accountability, local constraints, evidence requirements, or stop conditions.

## Repository Scope

This repository owns:

- Skill definitions and discovery material;
- versioned contracts and schemas;
- deterministic built-in handlers;
- packaging and validation;
- synthetic examples and tests;
- security policy and threat modeling;
- authoring and integration documentation.

It remains independent of ATLAS and DefenseOps.

### ATLAS — KNOW

[Cyber-Sentinel ATLAS](https://github.com/cyber-sentinel/Cyber-Sentinel-Atlas) owns canonical knowledge, ingestion, provenance, deterministic search, graph relationships, analyst investigation, and verified knowledge delivery.

Future ATLAS adapters may feed bounded context into Skills. Skill output is **not automatically authoritative ATLAS knowledge**.

### DefenseOps — DEFEND

[Cyber-Sentinel DefenseOps](https://github.com/cyber-sentinel/Cyber-Sentinel-DefenseOps) owns detection, hunt, validation, DFIR/IR, response, deception, and defensive-automation engineering content.

Skills may operationalize those artifacts without redefining their engineering ownership or validation maturity.

## Review Bundle

Create a reproducible review bundle with:

```bash
python -m cskills package --output ../skills-foundation-review.zip
```

The bundle includes license/notice material, source, contracts, examples, tests, docs, and a SHA-256 file inventory while excluding the Git database and build caches.

Checksums provide integrity evidence; they are **not** an authenticity signature and do not publish a release.

`python -m cskills release-check` validates the source and deliberately returns a pending-release state until owner release authority is satisfied.

## Governance & Licensing

Foundation v0.1 uses **Apache-2.0** for original project code, Skills, and documentation on this branch. Attribution and licensing material are recorded in:

- [LICENSE](LICENSE)
- [NOTICE](NOTICE)
- [LICENSE_STATUS.md](LICENSE_STATUS.md)

Licensing approval is not release approval.

The remaining merge blocker is repository-governance deployment/verification described in [docs/governance/main-protection.md](docs/governance/main-protection.md). Until that control is satisfied, this Foundation PR remains under review and should not be represented as an official public release.

## Engineering References

- [Contributing](CONTRIBUTING.md)
- [Security Reporting](SECURITY.md)
- [Research / Upstream Review](docs/research/upstream-review.md)
- [Governance Decisions](docs/governance/decisions.md)
- [Changelog](CHANGELOG.md)

## Design Principles

1. **Explicit over implicit.**
2. **Evidence over assumption.**
3. **Bounded capabilities over ambient authority.**
4. **Safe by default.**
5. **Human-reviewable.**
6. **Attributable and versioned.**
7. **Offline-capable where the Foundation contract requires it.**
8. **No ownership drift across Cyber-Sentinel products.**

---

<p align="center"><strong>Cyber-Sentinel Skills — APPLY with evidence.</strong></p>
<p align="center"><sub>Created and maintained by Ali RahimDabagh</sub></p>
