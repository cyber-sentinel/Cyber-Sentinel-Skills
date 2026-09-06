# Open owner decisions and engineering governance

Repository inspection: 2026-09-05; state rechecked on 2026-09-06.
Base `main`: `b62599a4de2c4c6050510047d0395ba40eb6e300`.
The initial tree contains only `README.md`. The repository is public, default
branch is `main`, automatic merge is disabled, `main` reports `protected: false`,
and the repository ruleset collection is empty. No repository setting was changed.

These are a dated inspection snapshot, not an assertion about future live settings.

## ARCHITECTURE ISSUE LIC-001 — project license

- **Initial problem:** the framework needed an explicit project license before
  representing its original work as a licensed reusable distribution.
- **Initial evidence:** the initial tree had no license file; repository metadata reported
  `license: null`; the owner's instruction explicitly prohibits silent selection.
- **Alternatives:** retain the pending status for architecture review; or have the
  owner explicitly choose a license and its code/documentation scope in a subsequent
  change. MIT and Apache-2.0 are examples to evaluate, not approved defaults.
- **Approved decision (2026-09-06):** the owner explicitly approved unmodified
  Apache-2.0 for original code, Skills and documentation, with NOTICE identifying
  Ali RahimDabagh and the canonical repository. The decision followed explanation
  of contribution control, permitted forks/commercial reuse and attribution limits.
- **Consequences:** LICENSE, NOTICE and SPDX metadata are included. Validation and
  bundle verification require those legal materials. Release authority remains
  separate; `release-check` reports `release-owner-approval-pending`. No upstream
  Skill/code import, release tag or publisher is authorized by this decision.
- **Status:** RESOLVED, adopted in the Foundation review branch. See
  [license and attribution](../../LICENSE_STATUS.md).

Apache permits forks; its attribution conditions do not require a credit banner
on every product screen. See the [license terms](https://www.apache.org/licenses/LICENSE-2.0).
The [contribution rules](../../CONTRIBUTING.md) reserve acceptance and roadmap
decisions to the owner independently of reuse rights under Apache-2.0.

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
verified main protection, and successful final review and CI. The license condition
is now fulfilled. Protection deployment still needs administrative application
and verification; final review and CI must cover the current PR head. New material
scope changes require their own decision. Public release remains separately
unapproved; auto-merge remains prohibited.

## Material decision protocol

Scope, project license, major architecture, technology lock-in, security boundary,
destructive action, public release and merge require owner decisions. Report an
`ARCHITECTURE ISSUE` with evidence, alternatives, recommendation and consequences.
Routine implementation defects inside the agreed offline architecture are fixed
autonomously. Do not expand permissions to make an example or test pass.

Latest `main` → feature branch → implementation → tests → CI → review → PR →
explicit owner merge approval. CI success and draft/ready status do not imply
that approval. No merge or release automation is configured.
