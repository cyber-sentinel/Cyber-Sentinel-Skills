# Open owner decisions and engineering governance

Repository inspection: 2026-09-05.
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

## ARCHITECTURE ISSUE GOV-001 — branch enforcement

- **Problem:** documented review/CI requirements are not yet enforced by repository
  protection. A user with suitable write access can bypass them.
- **Evidence:** `main` was unprotected and repository rulesets were empty at inspection.
- **Alternatives:** owner enforces the governance using a ruleset/protection policy;
  or retains a documented manual process and accepts the bypass risk.
- **Recommendation:** require PRs, the Foundation CI checks, and owner/code-owner
  review; dismiss stale approvals, block force pushes/deletion, and review any bypass
  permissions. A sole owner should assess how self-authored PR approval is handled
  before imposing an impossible review configuration.
- **Consequences:** `.github/CODEOWNERS` documents ownership but is not enforcement
  on its own. No settings were silently changed. This does not prevent review of
  the foundation PR, but should be resolved before treating governance as enforced.
- **Status:** OPEN, owner security-governance decision required.

## Material decision protocol

Scope, project license, major architecture, technology lock-in, security boundary,
destructive action, public release and merge require owner decisions. Report an
`ARCHITECTURE ISSUE` with evidence, alternatives, recommendation and consequences.
Routine implementation defects inside the agreed offline architecture are fixed
autonomously. Do not expand permissions to make an example or test pass.

Latest `main` → feature branch → implementation → tests → CI → review → PR →
explicit owner merge approval. CI success and draft/ready status do not imply
that approval. No merge or release automation is configured.
