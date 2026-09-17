# Cyber-Sentinel-Skills

**Governed Cybersecurity Operational Skills & Playbooks — APPLY**

[Cyber-Sentinel Ecosystem](https://github.com/cyber-sentinel)

Cyber-Sentinel-Skills is the **APPLY** layer of the Cyber-Sentinel ecosystem: a governed repository for reusable cybersecurity procedures and playbooks that make security work explicit, reviewable, attributable, repeatable, and suitable for consistent execution by humans and, where appropriate, AI-assisted workflows.

The product objective is to convert undocumented analyst know-how into **operational contracts** with clear scope, authorization boundaries, prerequisites, steps, evidence expectations, decision points, failure conditions, outputs, and governance.

> **Current maturity:** Foundation / operating-model stage
> **Repository visibility:** Public source repository
> **Primary audience:** SOC, Incident Response, DFIR, Threat Hunting, Security Engineering, GRC/operations, platform teams, and AI-assisted security operations
> **Operating posture:** Vendor-neutral first, evidence-driven, safe-by-default, human-reviewable
> **Licensing note:** No project `LICENSE` is currently published; public visibility does not grant reuse or redistribution rights

## Commercial Positioning

Security organizations often have strong people but weakly standardized operating knowledge. Critical procedures may exist only in senior analysts’ experience, informal chat threads, local documents, or tool-specific runbooks. That creates execution variance, onboarding friction, inconsistent evidence collection, automation risk, and operational dependency on individuals.

Cyber-Sentinel-Skills addresses that problem by treating procedures as **governed, reviewable operating assets** rather than informal command lists.

For security leaders and operations teams, the intended value is:

- reduce analyst-to-analyst execution variance;
- preserve operational knowledge beyond individual team members;
- accelerate onboarding without hiding critical judgment points;
- make authorization, destructive actions, stop conditions, and rollback explicit;
- standardize evidence collection and verification;
- improve handoff between SOC, THIR, DFIR, engineering, and governance teams;
- provide a safer foundation for AI-assisted execution;
- turn lessons learned into reusable, versioned operating practice.

**Core question:** *How should this security task be performed consistently, safely, and verifiably?*

## What a Skill Represents

A Skill is not merely a sequence of commands. It is a **governed execution contract** for an authorized cybersecurity task.

A substantive Skill should define, where applicable:

1. **Purpose** — the intended security outcome.
2. **Scope** — systems, platforms, telemetry, roles, and environments covered.
3. **Authorization & Safety** — required permissions, change boundaries, destructive actions, and prohibited shortcuts.
4. **Prerequisites** — access, tools, evidence, dependencies, and upstream context.
5. **Inputs** — information required before execution.
6. **Procedure** — ordered steps, branches, and decision points.
7. **Evidence & Verification** — how important actions and outcomes are proven.
8. **Failure / Exit Conditions** — when to stop, escalate, roll back, or request review.
9. **Expected Outputs** — reports, artifacts, tickets, findings, detections, or state changes.
10. **References & Attribution** — authoritative upstream material and provenance.
11. **Version History** — meaningful procedural changes over time.

A Skill should remain usable without relying on undocumented institutional knowledge.

## Product Boundaries

Skills owns the **repeatable operating method**. It does not silently absorb the responsibilities of other Cyber-Sentinel products.

Skills is **not**:

- the canonical cyber-defense knowledge graph or analyst investigation platform — that is ATLAS;
- the repository that owns detections, hunts, validation fixtures, or response engineering — that is DefenseOps;
- a collection of undocumented shell commands;
- a substitute for authorization, analyst judgment, or environment-specific change control;
- a mechanism for bypassing provenance, attribution, peer review, or safety controls;
- an autonomous-execution guarantee merely because a procedure is machine-readable.

## Enterprise Use Cases

The repository is designed to support operating methods across areas such as:

- SOC triage and alert investigation;
- threat hunting;
- incident response;
- DFIR evidence collection and analysis;
- detection validation and tuning workflows;
- security monitoring and telemetry verification;
- identity and access security operations;
- endpoint, network, cloud, and application-security operations;
- vulnerability and exposure-management workflows;
- AppSec and DevSecOps procedures;
- cyber-deception operations;
- security automation review and operational handoff;
- post-incident validation, lessons learned, and control improvement.

Specific products may be referenced where necessary, but the underlying method should remain as portable and vendor-neutral as practical.

## Design Principles

- **Explicit over implicit.** Critical operating knowledge should not exist only in an analyst's head.
- **Evidence over assumption.** Important actions and decisions should be verifiable.
- **Vendor-neutral first.** Product-specific implementation should be separated from the underlying method where practical.
- **Safe by default.** Authorization, destructive actions, stop conditions, and rollback must be clear.
- **Human-reviewable.** AI-agent usability must not make procedures opaque to people.
- **Attributable.** Upstream sources, standards, and engineering artifacts retain provenance.
- **Reusable without ownership drift.** Referencing ATLAS or DefenseOps content does not transfer ownership of those artifacts to Skills.
- **Governed evolution.** Procedures improve through evidence, review, and operating feedback rather than uncontrolled contribution volume.
- **Environment-aware.** Reusable procedure still requires explicit local assumptions and validation points.

## Human + AI Operating Model

Skills is designed to support human operators and AI-assisted workflows without collapsing accountability.

```text
Authorized task
      ↓
Bounded Skill / procedure
      ↓
Human or AI-assisted execution
      ↓
Evidence collection + verification
      ↓
Review / escalation / rollback as required
      ↓
Recorded outcome + lessons learned
```

AI-assisted execution does not remove the need for authorization, environment-specific constraints, human review, or evidence. Procedures that can change production state must make those boundaries explicit.

## Enterprise Control Model

A production-oriented Skill should be able to answer five governance questions before execution:

- **Who is authorized to perform or approve this action?**
- **What systems and data are in scope?**
- **What evidence proves the action and outcome?**
- **What conditions require stop, escalation, or rollback?**
- **What record remains after execution for review or audit?**

This makes Skills suitable for environments where repeatability, auditability, human oversight, and controlled automation matter as much as technical speed.

## Cyber-Sentinel Ecosystem

Cyber-Sentinel uses three contract-separated product layers:

```text
Cyber-Sentinel
├── ATLAS       — KNOW   → Connect • Search • Investigate • Explain
├── DefenseOps  — DEFEND → Detect • Hunt • Validate • Respond • Automate
└── Skills      — APPLY  → Execute • Review • Reuse • Govern
```

### ATLAS — KNOW

[Cyber-Sentinel-Atlas](https://github.com/cyber-sentinel/Cyber-Sentinel-Atlas) owns governed cyber-defense knowledge, canonical relationships, deterministic retrieval, provenance, investigation context, verified offline knowledge delivery, and analyst-facing product interfaces.

**Core question:** *What do we know about what we are seeing — and what evidence supports it?*

### DefenseOps — DEFEND

[Cyber-Sentinel-DefenseOps](https://github.com/cyber-sentinel/Cyber-Sentinel-DefenseOps) owns defensive engineering content: detections, hunts, validation assets, response engineering, DFIR/IR material, deception-oriented content, and defensive automation.

**Core question:** *What can we detect, validate, hunt, and defend — and what evidence supports that claim?*

### Skills — APPLY

Skills owns the reusable operating procedure used to execute a security task consistently and verifiably.

Skills may reference ATLAS knowledge and DefenseOps engineering artifacts, but it does not redefine their canonical contracts or silently copy ownership of their content.

## Governance & Contribution Model

The official Cyber-Sentinel-Skills line remains **maintainer-governed**.

Opening a pull request does not grant merge authority or permission to change the product direction. Contributions should preserve:

- attribution and provenance;
- technical correctness;
- scope discipline;
- authorization and safety boundaries;
- ecosystem ownership boundaries;
- version clarity;
- reviewability and evidence expectations.

Until a formal contribution-rights and project-license policy is published, contributions and reuse should be treated conservatively. The absence of a `LICENSE` file must not be interpreted as an open-source grant.

## Security & Authorization Boundary

Skills are intended for **authorized cybersecurity operations, controlled environments, defensive engineering, incident response, and security research**.

A documented procedure is not automatic authorization to execute it. Operators remain responsible for:

- legal authority;
- organizational approval;
- environment-specific risk;
- production change control;
- data handling requirements;
- rollback and recovery readiness.

Procedures that cannot establish their authorization or safety preconditions should stop or escalate rather than continue by assumption.

## Product & Commercial Maturity

Cyber-Sentinel-Skills is currently in a **foundation / operating-model stage**. The core product model is established, while broad production content coverage and formal public-release governance remain future work.

Current maturity boundaries are explicit:

- public repository visibility is for inspectability and collaboration;
- no project `LICENSE` is currently published;
- no claim is made that every procedure is production-certified across all environments;
- human-review and authorization boundaries remain mandatory even for machine-readable Skills;
- product quality is measured by clarity, evidence, safety, portability, and governance — not repository volume.

This is deliberate: a small set of trustworthy procedures is more valuable than a large collection of ambiguous playbooks.

## Product Direction

Near-term priorities are:

- establish a durable Skill schema and authoring standard;
- build a high-quality baseline of operational procedures;
- formalize evidence and verification patterns;
- strengthen safe human/AI operating boundaries;
- preserve contribution and attribution governance;
- improve interoperability with ATLAS knowledge and DefenseOps engineering artifacts;
- support reviewable, versioned operational improvement.

The objective is to create **reliable operating knowledge that security teams can trust, review, adapt, automate selectively, and govern**.

---

**Maintainer:** Ali RahimDabagh

**Ecosystem role:** `APPLY`

**Focus:** Operational Security Methods • SOC/IR/DFIR Procedures • Security Engineering • AI-Assisted Security Operations • Governance
