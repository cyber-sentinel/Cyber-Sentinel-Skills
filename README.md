# Cyber-Sentinel-Skills

**Vendor-neutral Cybersecurity Operational Skills & Playbooks — APPLY**

[Cyber-Sentinel Profile](https://github.com/cyber-sentinel)

Cyber-Sentinel-Skills is the **APPLY** layer of the Cyber-Sentinel ecosystem: a repository for reusable, reviewable, attributable, and repeatable cybersecurity procedures and playbooks that can be followed by both humans and AI agents.

The goal is to convert security work from implicit analyst know-how into explicit operating methods with clear scope, prerequisites, steps, verification, evidence expectations, limitations, and governance.

> **Repository status:** Foundation stage. The repository is public, but no project license is currently present; public visibility alone does not grant reuse or redistribution rights.

## Mission

Make cybersecurity operations explicit enough to be executed consistently, reviewed technically, improved over time, and reused without losing context or accountability.

**Core question:** *How should this security task be performed consistently?*

## Product Position

Skills is **not**:

- the canonical cyber-defense knowledge graph or investigation platform — that is Atlas;
- the repository that owns detections, hunts, validation artifacts, and response engineering — that is DefenseOps;
- a collection of undocumented command snippets;
- a substitute for analyst judgment, authorization, or environment-specific change control;
- a mechanism for bypassing provenance, attribution, safety, or technical review.

Skills owns the **repeatable operating method**: how an authorized security task should be prepared, executed, verified, reviewed, and governed.

## Cyber-Sentinel Ecosystem

Cyber-Sentinel is intentionally a **contract-separated ecosystem** with three current project layers:

```text
Cyber-Sentinel
├── Atlas       — KNOW   → Connect • Search • Investigate • Explain
├── DefenseOps  — DEFEND → Detect • Hunt • Validate • Respond • Automate
└── Skills      — APPLY  → Execute • Review • Reuse • Govern
```

### Atlas — KNOW

[Cyber-Sentinel-Atlas](https://github.com/cyber-sentinel/Cyber-Sentinel-Atlas) owns governed cyber-defense knowledge, canonical relationships, deterministic retrieval, provenance, investigation context, offline knowledge delivery, and analyst-facing product interfaces.

**Core question:** *What do we know about what we are seeing?*

### DefenseOps — DEFEND

[Cyber-Sentinel-DefenseOps](https://github.com/cyber-sentinel/Cyber-Sentinel-DefenseOps) owns defensive engineering content: detections, hunts, validation assets, response engineering, DFIR/IR material, deception-oriented content, and defensive automation.

**Core question:** *What can we detect, validate, hunt, and defend?*

### Skills — APPLY

Cyber-Sentinel-Skills owns reusable operational procedures and playbooks that make cybersecurity tasks explicit, reviewable, attributable, repeatable, and usable by both humans and AI agents.

Skills can reference Atlas knowledge and DefenseOps engineering artifacts, but it does not redefine their canonical contracts or silently copy ownership of their content.

### Ecosystem Operating Loop

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

`KNOW → DEFEND → APPLY → VALIDATE → AUTOMATE → EVOLVE`

## What Belongs in a Skill

A substantive operational skill should make the execution contract clear. Depending on the task, it should define:

1. **Purpose** — what security outcome the skill is intended to achieve.
2. **Scope** — systems, platforms, telemetry, roles, and environments to which it applies.
3. **Authorization & Safety** — required permissions, change boundaries, and actions that must not be performed without approval.
4. **Prerequisites** — access, tools, evidence, data sources, and dependencies.
5. **Inputs** — information the operator or agent needs before execution.
6. **Procedure** — ordered, explicit steps with decision points where necessary.
7. **Evidence & Verification** — how to prove each important step or outcome.
8. **Failure / Exit Conditions** — when to stop, escalate, roll back, or request review.
9. **Expected Outputs** — reports, artifacts, tickets, detections, findings, or state changes.
10. **References & Attribution** — authoritative sources and upstream material.
11. **Version History** — meaningful changes to the procedure over time.

A skill should be usable without requiring undocumented institutional knowledge.

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

Specific tools or products may be referenced where necessary, but the underlying skill should remain as portable and vendor-neutral as practical.

## Design Principles

- **Explicit over implicit.** Critical knowledge should not exist only in an operator's head.
- **Evidence over assumption.** Important actions and decisions should be verifiable.
- **Vendor-neutral first.** Product-specific instructions should be separated from the underlying operating method where practical.
- **Safe by default.** Authorization, destructive actions, rollback, and stop conditions must be clear.
- **Human-reviewable.** AI-agent usability must not make the procedure opaque to people.
- **Attributable.** Upstream ideas, standards, and source material must retain provenance.
- **Reusable without ownership drift.** Referencing Atlas or DefenseOps content does not transfer ownership of those artifacts to Skills.
- **Governed evolution.** Procedures should improve through review and operational feedback rather than uncontrolled contribution volume.

## Contribution & Governance Direction

Opening a pull request does not grant merge authority or change the official project direction.

The official Cyber-Sentinel-Skills line remains maintainer-governed. Contributions should preserve attribution, technical quality, scope discipline, safety boundaries, and compatibility with the Cyber-Sentinel ecosystem model.

Until a formal contribution-rights and project-license policy is published, contributions and reuse should be treated conservatively. The absence of a `LICENSE` file must not be interpreted as an open-source grant.

## Safety

Skills are intended for authorized cybersecurity operations, controlled environments, defensive engineering, incident response, and security research.

A documented procedure is not automatic authorization to execute it. Operators remain responsible for legal authority, organizational approval, environment-specific risk, and change-control requirements.

---

**Maintainer:** Ali RahimDabagh  
**Profile:** `cyber-sentinel`  
**Role in ecosystem:** `APPLY`
