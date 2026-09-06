# Open owner decisions and engineering governance

Repository inspection: 2026-09-05; state rechecked on 2026-09-06.
Base `main`: `b62599a4de2c4c6050510047d0395ba40eb6e300`.
The initial tree contains only `README.md`. The repository is public, default
branch is `main`, automatic merge is disabled, `main` reports `protected: false`,
and the repository ruleset collection is empty. No repository setting was changed.

These are a dated inspection snapshot, not an assertion about future live settings.

## ARCHITECTURE ISSUE LIC-001 — project license

- **Problem:** no project license is approved. The framework is intended to be
  reusable, but a project-level redistribution license cannot be assumed.
- **Evidence:** initial tree has no license file; repository metadata reports
  `license: null`; the owner's instruction explicitly prohibits silent selection.
- **Alternatives:** retain the pending status for architecture review; or have the
  owner explicitly choose a license and its code/documentation scope in a subsequent
  change. MIT and Apache-2.0 are examples to evaluate, not approved defaults.
- **Recommendation:** retain pending status for this review candidate. Record the
  owner's exact license choice and scope before release or external material import.
- **Consequences:** no `LICENSE`, SPDX license claim, release tag or publisher is
  added. Manifests/bundles mark the decision pending. `release-check` rejects release
  readiness. Original engineering work and the explicitly requested PR can proceed.
- **Status:** OPEN, owner decision required. See [license status](../../LICENSE_STATUS.md).

Owner follow-up, 2026-09-06: license approval remains withheld pending clarity on
roadmap control and source attribution. The proposal is unmodified Apache-2.0 for
original code, Skills and documentation, with appropriate copyright attribution
and a NOTICE identifying Ali RahimDabagh and the canonical repository. This is
not yet adopted. Apache permits forks; its attribution conditions do not require
a credit banner on every product screen. See the
[license terms, sections 4 and 6](https://www.apache.org/licenses/LICENSE-2.0).
The [contribution rules](../../CONTRIBUTING.md) reserve acceptance and roadmap
decisions to the owner independently of the eventual reuse license.

## ARCHITECTURE ISSUE GOV-001 — branch enforcement

- **Problem:** documented review/CI requirements are not yet enforced by repository
  protection. A user with suitable write access can bypass them.
- **Evidence:** `main` was unprotected and repository rulesets were empty at inspection.
- **Alternatives:** owner enforces the governance using a ruleset/protection policy;
  or retains a documented manual process and accepts the bypass risk.
- **Approved decision (2026-09-06):** require PRs and the Foundation CI checks;
  block force pushes and branch deletion. Keep explicit owner merge authorization
  as project policy. Do not require a second reviewer before an independent
  reviewer is designated. The [exact settings](main-protection.md) distinguish
  this initial profile from future enforcement with multiple maintainers.
- **Consequences:** `.github/CODEOWNERS` documents ownership but is not enforcement
  on its own. No settings were silently changed. This does not prevent review of
  the foundation PR, but should be resolved before treating governance as enforced.
- **Status:** APPROVED, awaiting administrative configuration and verification.
  The connected GitHub tools cannot administer branch protection. The live read
  on 2026-09-06 still reports `main` as unprotected and an empty ruleset collection.

## Owner authorization — Foundation PR #1

On 2026-09-06 the owner explicitly approved conditional merge of
[PR #1](https://github.com/cyber-sentinel/Cyber-Sentinel-Skills/pull/1), covering the
existing Foundation v0.1 scope. This approval persists; it is not a merge event.
Its conditions are an explicitly chosen and recorded project license, applied and
verified main protection, and successful final review and CI. License choice and
protection deployment are still outstanding. New material scope changes require
their own decision. Public release remains separately unapproved; auto-merge
remains prohibited.

## Material decision protocol

Scope, project license, major architecture, technology lock-in, security boundary,
destructive action, public release and merge require owner decisions. Report an
`ARCHITECTURE ISSUE` with evidence, alternatives, recommendation and consequences.
Routine implementation defects inside the agreed offline architecture are fixed
autonomously. Do not expand permissions to make an example or test pass.

Latest `main` → feature branch → implementation → tests → CI → review → PR →
explicit owner merge approval. CI success and draft/ready status do not imply
that approval. No merge or release automation is configured.
