# Approved main protection profile

Approved by the owner on 2026-09-06 under [GOV-001](decisions.md).
Status: **applied and verified on 2026-10-24**. The existing classic
[branch protection rule](https://github.com/cyber-sentinel/Cyber-Sentinel-Skills/settings/branch_protection_rules/85291148)
was already present when inspected; no duplicate rule was created. The connected
GitHub integration returned 403 for the administration-only protection endpoint,
so the full settings were read back in the authenticated GitHub browser. The
public branch API independently returned `protected: true` for `main`.

## GOV-001 verification evidence — 2026-10-24

- Rule pattern is exactly `main`, and the edit page reports **Applies to 1 branch: main**.
- Require a pull request before merging: on. Require approvals: off (zero
  mandatory reviews). Code Owners review and most-recent-push approval: off.
- Require status checks: on; require branches to be up to date: on. Exactly
  the four checks listed below are required, each with GitHub Actions as source.
- Do not allow bypassing: on, including administrators and bypass-capable roles.
  Classic branch protection has no configured bypass-exception list in this rule.
- Allow force pushes: off; allow deletions: off. Repository-wide auto-merge: off.
- The repository rulesets page reported **no rulesets**, so no overlapping
  repository ruleset was found. The saved rule was reopened and read back;
  no direct push to `main` was attempted.
- At verification time, the exact-head [Foundation workflow run](https://github.com/cyber-sentinel/Cyber-Sentinel-Skills/actions/runs/40037385468)
  had succeeded at PR #1 head `22ee6ba1ec2f61eac6ea82ff5ba5982745421886`.
  Its four matrix jobs have the exact names below and completed successfully.
  A later documentation commit needs its own exact-head CI. PR #1 remains Draft;
  its `README.md` merge conflict and final review are
  separate blockers. This verification is not merge or release authorization.

## Approved profile and future maintenance

In this repository's [branch settings](https://github.com/cyber-sentinel/Cyber-Sentinel-Skills/settings/branches),
maintain the existing classic rule targeting exactly `main`. Inspect any new
overlapping rules before changing it; do not create a duplicate. The approved
settings are:

| Setting | Value |
| --- | --- |
| Branch name pattern | `main` |
| Require a pull request before merging | Enabled |
| Require approvals | Disabled in this initial profile |
| Require review from Code Owners | Disabled in this initial profile |
| Require approval of the most recent reviewable push | Disabled in this initial profile |
| Require status checks to pass before merging | Enabled; all four checks below |
| Require branches to be up to date before merging | Enabled |
| Do not allow bypassing the above settings | Enabled, including administrators |
| Allow force pushes | Disabled |
| Allow deletions | Disabled |

Leave bypass exceptions empty. Keep auto-merge disabled. Require these exact
job names, observed in the Foundation CI run; select GitHub Actions as their
expected source where the interface offers a source selector:

- `validate (ubuntu-24.04, Python 3.11)`
- `validate (ubuntu-24.04, Python 3.12)`
- `validate (windows-2022, Python 3.11)`
- `validate (windows-2022, Python 3.12)`

If a check is absent from the selector during future maintenance, inspect a
recent Foundation CI run and its exact job names before saving; do not
substitute an unrelated check.
GitHub documents [setup](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
and [protection behavior](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

## Review authority and verification

This initial profile enforces PRs and CI. It does not technically enforce an owner
review against another person or app with merge permission. Explicit owner merge
authorization remains mandatory under [project instructions](../../AGENTS.md).
Before adding another writer or maintainer, review the access list and adopt an
owner-approved review configuration; account for self-authored PRs before enabling
required approvals or Code Owner approval. CODEOWNERS is not an access-control list.

After any future change, verify the saved settings and all four required checks on PR #1.
A public `protected: true` flag alone does not prove the required settings are
correct. Record administrative readback or owner-provided settings evidence;
do not infer future settings from this dated verification. Do not probe by pushing to main.

If an incorrect setting blocks valid work, the administrator should correct that
specific setting after review. Record the correction; do not bypass the gate or
delete protection just to complete a merge. Repository content rollback remains
a normal revert PR. Changes to this approved profile require an owner decision.
