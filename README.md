<h1 align="center">Cyber-Sentinel Skills</h1>
<p align="center"><strong>Governed Cybersecurity Operational Skills & Playbooks</strong></p>
<p align="center">APPLY • EXECUTE • REVIEW • REUSE • GOVERN</p>

<p align="center">
  <img alt="Foundation" src="https://img.shields.io/badge/maturity-Foundation-informational">
  <img alt="Foundation v0.1" src="https://img.shields.io/badge/Foundation%20v0.1-under%20review-blueviolet">
  <img alt="Safe by Default" src="https://img.shields.io/badge/design-safe--by--default-0f766e">
  <img alt="Human Reviewable" src="https://img.shields.io/badge/operation-human--reviewable-334155">
</p>

Cyber-Sentinel Skills is the **APPLY** layer of the Cyber-Sentinel ecosystem: a governed framework for turning analyst know-how into explicit, reviewable, attributable, and repeatable operating procedures for humans and, where appropriate, AI-assisted workflows.

> **Core question:** **How should this security task be performed consistently, safely, and verifiably?**

Skills is designed to reduce execution variance without hiding judgment, authorization, evidence requirements, or failure boundaries behind automation.

## Current State

| Boundary | State |
| --- | --- |
| Public `main` | Foundation / operating-model baseline |
| Foundation v0.1 implementation | **Under controlled review in [PR #1](https://github.com/cyber-sentinel/Cyber-Sentinel-Skills/pull/1)** |
| Official release | **Not authorized** |
| Production certification | **Not claimed** |
| Execution philosophy | bounded, deterministic where possible, safe-by-default, human-reviewable |
| Ecosystem role | **APPLY** |

The active Foundation v0.1 review branch contains a substantially deeper implementation and validation surface. That work remains separate from `main` until its governance gate is satisfied. This README does not represent unmerged candidate work as a released product.

## What a Skill Is

A Skill is not a command list. It is a **governed execution contract** for an authorized cybersecurity task.

A substantive Skill should define:

| Contract area | Required intent |
| --- | --- |
| **Purpose** | the security outcome the procedure is trying to achieve |
| **Scope** | systems, roles, platforms, data, and environments covered |
| **Authorization & Safety** | permissions, destructive boundaries, prohibited shortcuts |
| **Prerequisites** | access, evidence, tools, dependencies, upstream context |
| **Inputs** | information required before execution begins |
| **Procedure** | ordered steps, branches, and decision points |
| **Evidence & Verification** | what proves important actions and outcomes |
| **Failure / Exit Conditions** | when to stop, escalate, or roll back |
| **Outputs** | reports, artifacts, findings, tickets, or state changes |
| **References & Attribution** | authoritative sources and provenance |
| **Version History** | meaningful procedural evolution over time |

A Skill should remain understandable and reviewable without relying on undocumented institutional knowledge.

## Why Skills Exists

Security organizations often have strong practitioners but weakly standardized operational knowledge. Important procedures may live only in senior analysts’ experience, chat threads, local notes, or tool-specific runbooks.

That creates:

- analyst-to-analyst execution variance;
- onboarding friction;
- inconsistent evidence collection;
- fragile dependency on individuals;
- automation risk;
- unclear authorization and stop conditions;
- weak post-incident learning loops.

Skills treats procedures as **versioned operating assets** rather than informal memory.

## Human + AI Operating Model

```text
Authorized Task
      ↓
Bounded Skill Contract
      ↓
Human or AI-Assisted Execution
      ↓
Evidence Collection + Verification
      ↓
Review / Escalation / Rollback
      ↓
Recorded Outcome + Lessons Learned
```

AI-assisted execution does not remove authorization, environment-specific constraints, human accountability, or evidence requirements. A machine-readable procedure is **not** an autonomous-execution entitlement.

## Foundation v0.1 Candidate

The active [Foundation v0.1 review](https://github.com/cyber-sentinel/Cyber-Sentinel-Skills/pull/1) is building the executable foundation behind the operating model. Its reviewed scope includes:

- versioned Skill contracts and schemas;
- deterministic offline handlers;
- bounded input/output envelopes;
- explicit provenance and limitation fields;
- capability and authorization checks;
- synthetic positive/negative fixtures;
- reproducible review and integrity evidence;
- security and governance documentation;
- original exemplar Skills for evidence summarization, IOC normalization, evidence timelines, and detection-specification review.

Those capabilities are candidate-branch work until the Foundation PR is merged. The PR remains the authoritative place to inspect its exact implementation and current blocker state.

## Product Boundaries

Skills owns the **repeatable operating method**. It does not silently absorb the responsibilities of the other Cyber-Sentinel products.

Skills is **not**:

- the canonical knowledge graph or investigation platform — that is ATLAS;
- the owner of detections, hunts, or validation fixtures — that is DefenseOps;
- a shell-command collection;
- a substitute for analyst judgment or production change control;
- a mechanism for bypassing attribution, provenance, or authorization;
- an autonomous agent runtime merely because procedures can be machine-readable.

## Enterprise Use Cases

Skills is intended for reusable operating methods across:

`SOC Triage` • `Incident Response` • `DFIR` • `Threat Hunting` • `Detection Validation` • `Telemetry Verification` • `Identity Security` • `Endpoint / Network / Cloud Security` • `Vulnerability Management` • `AppSec / DevSecOps` • `Cyber Deception` • `Security Automation Review`

The underlying method should remain vendor-neutral where practical, with product-specific implementation details separated from the durable procedure.

## Design Principles

1. **Explicit over implicit.** Critical operating knowledge should not live only in an analyst’s head.
2. **Evidence over assumption.** Important actions and decisions should be verifiable.
3. **Vendor-neutral first.** Tool-specific implementation should not erase the underlying method.
4. **Safe by default.** Authorization, destructive actions, stop conditions, and rollback must be clear.
5. **Human-reviewable.** Agent usability must not make procedures opaque to people.
6. **Attributable.** Upstream sources and engineering artifacts retain provenance.
7. **Governed evolution.** Procedures improve through evidence and review, not uncontrolled volume.
8. **Environment-aware.** Reusability does not eliminate local validation requirements.

## Enterprise Control Questions

Before execution, a production-oriented Skill should be able to answer:

- **Who is authorized to perform or approve this action?**
- **What systems and data are in scope?**
- **What evidence proves the action and outcome?**
- **What conditions require stop, escalation, or rollback?**
- **What durable record remains for review or audit?**

## Cyber-Sentinel Ecosystem

```text
ATLAS       — KNOW   → Connect • Search • Investigate • Explain
DefenseOps  — DEFEND → Detect • Hunt • Validate • Respond • Automate
Skills      — APPLY  → Execute • Review • Reuse • Govern
```

### ATLAS — KNOW

[Cyber-Sentinel ATLAS](https://github.com/cyber-sentinel/Cyber-Sentinel-Atlas) owns canonical security knowledge, provenance, deterministic retrieval, relationships, investigation context, and verified offline delivery.

Skills may consume bounded ATLAS context, but Skill output does not automatically become canonical ATLAS truth.

### DefenseOps — DEFEND

[Cyber-Sentinel DefenseOps](https://github.com/cyber-sentinel/Cyber-Sentinel-DefenseOps) owns detection, hunt, validation, DFIR/IR, response, deception, and defensive-automation engineering artifacts.

Skills may operationalize those artifacts, but does not silently redefine their engineering ownership or validation maturity.

## Governance & Release Boundary

The official Skills line is maintainer-governed. Public visibility or an open PR does not grant merge authority, execution authorization, production approval, or release status.

Until governance and release conditions are satisfied:

- candidate implementation remains candidate implementation;
- release claims remain fail-closed;
- environment-specific approval remains mandatory;
- attribution and provenance remain part of the contract;
- product quality is measured by clarity, evidence, safety, portability, and governance — not repository volume.

## Product Direction

Near-term priorities are:

- complete the governed Foundation v0.1 boundary;
- establish durable Skill authoring and validation contracts;
- expand a small, high-quality set of operational Skills;
- strengthen evidence and verification patterns;
- preserve safe human/AI execution boundaries;
- improve interoperability with ATLAS and DefenseOps without ownership drift.

The objective is **reliable operating knowledge that teams can review, adapt, automate selectively, and govern**.

---

<p align="center"><strong>Cyber-Sentinel Skills — APPLY with evidence.</strong></p>
<p align="center"><sub>Maintained by Ali RahimDabagh</sub></p>
