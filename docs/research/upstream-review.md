# Internal design research: mukul975 references

Review date: 2026-09-05. Purpose: design inspiration and a bounded reference
comparison for Cyber Sentinel Skills Foundation v0.1. This note contains original
analysis and links; no upstream Skill, code, template, logo or dataset is imported.
It is an engineering note in a public repository and contains no private evidence.

## Sources inspected and licensing observations

| Repository and exact revision | Inspected material | License observation | Adoption status |
|---|---|---|---|
| [Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills/tree/54a798831d2266a3ca61ce68a7acb80b81160d57) | README, LICENSE, root inventory, a Volatility `SKILL.md` example | LICENSE identifies Apache-2.0; README agrees | Inspiration only; no import |
| [Threatswarm](https://github.com/mukul975/Threatswarm/tree/4789a8223ef5325f46a198059f56b97ff72ee26e) | README, LICENSE, `.claude/hooks/scope_check.py` | LICENSE identifies MIT, copyright 2026 Mahipal | Inspiration/rejection analysis only; no import |
| [cve-mcp-server](https://github.com/mukul975/cve-mcp-server/tree/d666bac3743574cecc98bcbf524558c2bf0d8e61) | README, LICENSE, root inventory | README badge says MIT; LICENSE contains Apache-2.0 | Conflicting license signals: block any import until clarified |

Exact license files:
[Skills LICENSE](https://github.com/mukul975/Anthropic-Cybersecurity-Skills/blob/54a798831d2266a3ca61ce68a7acb80b81160d57/LICENSE),
[Threatswarm LICENSE](https://github.com/mukul975/Threatswarm/blob/4789a8223ef5325f46a198059f56b97ff72ee26e/LICENSE),
[CVE LICENSE](https://github.com/mukul975/cve-mcp-server/blob/d666bac3743574cecc98bcbf524558c2bf0d8e61/LICENSE).

For a future Apache-2.0-derived distribution, review section 4: include the license,
mark changed files, retain applicable attribution and preserve relevant NOTICE
content when present. For substantial MIT-derived copies, retain the copyright
and permission notice. These observations do not complete a per-file provenance
audit. No root NOTICE file appeared in the inspected Skills/CVE root inventories;
that does not establish the absence of nested or third-party notices.

No current import relies on either license. Before any future adoption, inspect
the exact files and dependencies, verify ownership/attribution and notices, resolve
ambiguity, then record commit, paths, license, modifications and redistribution
requirements. Public visibility and badges are insufficient evidence by themselves.

## Useful concepts

The Skills reference demonstrates task-oriented directories, concise discovery
metadata, procedural guidance and supporting material. Its README advertises
818 Skills, while some sections still say 817; catalog size and compatibility
claims were not independently certified. Foundation uses four original exemplars
and behavioral tests rather than adopting that catalog or its completeness claims.
See [the pinned README](https://github.com/mukul975/Anthropic-Cybersecurity-Skills/blob/54a798831d2266a3ca61ce68a7acb80b81160d57/README.md).

Threatswarm's separation of agent instructions and a pre-tool policy hook is a
useful architectural topic. However, the inspected root hook explicitly permits
execution when scope is absent/empty, input JSON is malformed, or no target is
extracted. Its command classification is heuristic. These are observations about
that exact file and revision, not a tested claim about every packaged variant.
See [the inspected hook](https://github.com/mukul975/Threatswarm/blob/4789a8223ef5325f46a198059f56b97ff72ee26e/.claude/hooks/scope_check.py).

CVE MCP Server illustrates separating security-source access from agent-facing
tools, and documents multiple data providers and orchestration. That is relevant
to future adapters, not a reason to make MCP or live API dependencies canonical
in this foundation. Its security and provider claims were not exercised against
live services. See [the pinned README](https://github.com/mukul975/cve-mcp-server/blob/d666bac3743574cecc98bcbf524558c2bf0d8e61/README.md).

## Concepts rejected or deferred

- Importing a large Skill catalog before verifying correctness, permissions and licenses.
- Treating missing scope or malformed policy input as permission to proceed.
- Treating command-string target extraction as a complete egress security boundary.
- Treating claimed framework mappings as independently verified cybersecurity facts.
- Binding core identity/schema to one model vendor, a pentest kill chain or MCP.
- Adding credential extraction, hidden persistence, arbitrary shell or live targets
  to the passive Foundation profile.

## Independent Cyber Sentinel implementation

Implement a versioned JSON contract with explicit resource/effect metadata;
deterministic host authorization; no dynamic code loading; four narrow offline
handlers; bounded input/output; source-bearing result envelopes; explicit limits;
negative tests; reproducible review packaging and CI. These are original source
and fixtures written for the approved project scope.

Use the [Agent Skills specification](https://agentskills.io/specification) for
discovery compatibility. `SKILL.md` plus a JSON contract is independently designed;
loading Markdown alone into another host does not enforce Cyber Sentinel policy.
No mukul975 content is imported into this repository or into Atlas.
