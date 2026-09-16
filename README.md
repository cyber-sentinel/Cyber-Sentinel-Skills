# Cyber-Sentinel-Skills

**Governed Cybersecurity Operational Skills & Playbooks — APPLY**

[Cyber-Sentinel Ecosystem](https://github.com/cyber-sentinel)

Cyber-Sentinel-Skills is the **APPLY** layer of the Cyber-Sentinel ecosystem: a governed repository for reusable cybersecurity procedures and playbooks that make security work explicit, reviewable, attributable, repeatable, and suitable for consistent execution by humans and, where appropriate, AI agents.

The product objective is to convert undocumented analyst know-how into **operational contracts** with clear scope, authorization boundaries, prerequisites, steps, evidence expectations, decision points, failure conditions, outputs, and governance.

> **Current maturity:** Foundation stage
> **Repository visibility:** Public
> **Primary audience:** SOC, Incident Response, DFIR, Threat Hunting, Security Engineering, GRC/operations, platform teams, and AI-assisted security workflows
> **Operating posture:** Vendor-neutral first, evidence-driven, safe-by-default, human-reviewable
> **Licensing note:** No project `LICENSE` is currently present; public visibility does not grant reuse or redistribution rights

## Why Skills Exists

Security operations frequently depend on tacit knowledge: experienced analysts know which checks matter, when to stop, what evidence to collect, which actions are destructive, and how to verify success — but that knowledge often remains undocumented or buried in informal runbooks.

Skills turns that implicit knowledge into explicit operating methods that can be:

- executed consistently;
- technically reviewed;
- versioned and improved;
- attributed to authoritative sources;
- evaluated by evidence rather than assumption;
- reused across teams without losing safety or context;
- consumed by AI-assisted workflows without making the procedure opaque to people.

**Core question:** *How should this security task be performed consistently, safely, and verifiably?*

## Product Value

Cyber-Sentinel-Skills is intended to help security organizations:

- reduce analyst-to-analyst execution variance;
- preserve operational knowledge beyond individual team members;
- make authorization and destructive-action boundaries explicit;
- standardize evidence collection and verification;
- improve handoff between SOC, THIR, DFIR, engineering, and governance teams;
- create reviewable procedures for AI-assisted security operations;
- separate reusable operating method from vendor-specific implementation details;
- feed lessons learned back into better procedures, detections, and knowledge.

## What a Skill Represents

A Skill is not merely a command list. It is a **governed execution contract** for an authorized cybersecurity task.

A substantive Skill should define, as applicable:

1. **Purpose** — the intended security outcome.
2. **Scope** — systems, platforms, telemetry, roles, and environments covered.
3. **Authorization & Safety** — required permissions, change boundaries, destructive actions, and prohibited shortcuts.
4. **Prerequisites** — access, tools, evidence, dependencies, and upstream context.
5. **Inputs** — information required before execution.
6. **Procedure** — ordered steps and decision points.
7. **Evidence & Verification** — how important actions and outcomes are proven.
8. **Failure / Exit Conditions** — when to stop, escalate, roll back, or request review.
9. **Expected Outputs** — reports, artifacts, tickets, findings, detections, or state changes.
10. **References & Attribution** — authoritative upstream material and provenance.
11. **Version History** — meaningful procedural changes over time.

A Skill should be usable without requiring undocumented institutional knowledge.

## Product Boundaries

Skills owns the **repeatable operating method**. It does not silently absorb the responsibilities of other Cyber-Sentinel products.

Skills is **not**:

- the canonical cyber-defense knowledge graph or analyst investigation platform — that is ATLAS;
- the repository that owns detections, hunts, validation fixtures, or response engineering — that is DefenseOps;
- a collection of undocumented shell commands;
- a substitute for authorization, analyst judgment, or environment-specific change control;
- a mechanism for bypassing provenance, attribution, peer review, or safety controls;
- an autonomous-execution guarantee merely because a procedure is machine-readable.

## Intended Skill Domains

The repository is designed to support vendor-neutral operating methods across areas such as:

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

Specific tools or products may be referenced when necessary, but the underlying procedure should remain as portable and vendor-neutral as practical.

## Design Principles

- **Explicit over implicit.** Critical operating knowledge should not exist only in an analyst's head.
- **Evidence over assumption.** Important actions and decisions should be verifiable.
- **Vendor-neutral first.** Product-specific implementation should be separated from the underlying method where practical.
- **Safe by default.** Authorization, destructive actions, stop conditions, and rollback must be clear.
- **Human-reviewable.** AI-agent usability must not make procedures opaque to people.
- **Attributable.** Upstream sources, standards, and engineering artifacts retain provenance.
- **Reusable without ownership drift.** Referencing ATLAS or DefenseOps content does not transfer ownership of those artifacts to Skills.
- **Governed evolution.** Procedures improve through evidence, review, and operating feedback rather than uncontrolled contribution volume.
- **Environment-aware.** A reusable procedure must still identify assumptions that require local validation.

## Human + AI Operating Model

Skills is designed to support both human operators and AI-assisted workflows without collapsing accountability.

The intended model is:

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

AI execution does not remove the need for authorization, environment-specific constraints, human review, or evidence. Procedures that can change production state must make those boundaries explicit.

## Cyber-Sentinel Ecosystem

Cyber-Sentinel uses three contract-separated layers:

```text
Cyber-Sentinel
├── ATLAS       — KNOW   → Connect • Search • Investigate • Explain
├── DefenseOps  — DEFEND → Detect • Hunt • Validate • Respond • Automate
└── Skills      — APPLY  → Execute • Review • Reuse • Govern
```

### ATLAS — KNOW

[Cyber-Sentinel-Atlas](https://github.com/cyber-sentinel/Cyber-Sentinel-Atlas) owns governed cyber-defense knowledge, canonical relationships, deterministic retrieval, provenance, investigation context, verified offline knowledge delivery, and analyst-facing product interfaces.

**Core question:** *What do we know about what we are seeing?*

### DefenseOps — DEFEND

[Cyber-Sentinel-DefenseOps](https://github.com/cyber-sentinel/Cyber-Sentinel-DefenseOps) owns defensive engineering content: detections, hunts, validation assets, response engineering, DFIR/IR material, deception-oriented content, and defensive automation.

**Core question:** *What can we detect, validate, hunt, and defend?*

### Skills — APPLY

Skills owns the reusable procedure used to execute a security task consistently and verifiably.

Skills may reference ATLAS knowledge and DefenseOps engineering artifacts, but it does not redefine their canonical contracts or silently copy ownership of their content.

### Operating Loop

```text
Authoritative Sources / Telemetry / Security Knowledge
                         │
                         ▼
                  ATLAS — KNOW
        Connect • Search • Investigate • Explain
                         │
             evidence / defensive context
                         ▼
               DefenseOps — DEFEND
       Detect • Hunt • Validate • Respond • Automate
                         │
              repeatable operating method
                         ▼
                  Skills — APPLY
          Execute • Review • Reuse • Govern
                         │
                         ▼
          VALIDATE → AUTOMATE → EVOLVE
                         │
                         └──────────────↺
                    feedback into knowledge,
                 engineering and procedures
```

`VALIDATE`, `AUTOMATE`, and `EVOLVE` are ecosystem operating outcomes and feedback stages, not separate repositories.

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

## Safety & Authorization

Skills are intended for **authorized cybersecurity operations, controlled environments, defensive engineering, incident response, and security research**.

A documented procedure is not automatic authorization to execute it. Operators remain responsible for:

- legal authority;
- organizational approval;
- environment-specific risk;
- production change control;
- data handling requirements;
- rollback and recovery readiness.

Procedures that cannot establish their authorization or safety preconditions should stop or escalate rather than continue by assumption.

## Product Direction

The near-term direction is to establish a durable Skill format and a high-quality baseline of operational procedures before expanding breadth.

Priorities include:

- clear reusable execution contracts;
- evidence and verification patterns;
- safe human/AI operating boundaries;
- contribution and attribution governance;
- interoperability with ATLAS knowledge and DefenseOps engineering artifacts;
- reviewable, versioned operational improvement.

The objective is not to maximize the number of playbooks. It is to create **reliable operating knowledge that security teams can trust, review, adapt, and govern**.

---

**Maintainer:** Ali RahimDabagh

**Profile:** `cyber-sentinel`

**Ecosystem role:** `APPLY`

**Focus:** Operational Security Methods • SOC/IR/DFIR Procedures • Security Engineering • AI-Assisted Operations • Governance
