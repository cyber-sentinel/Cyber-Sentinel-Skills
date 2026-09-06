# Approved main protection profile

Approved by the owner on 2026-09-06 under [GOV-001](decisions.md).
Status: configuration prepared; **not applied or verified**.
The connected GitHub tools do not provide repository administration.

## Administrative setup

In this repository's [branch settings](https://github.com/cyber-sentinel/Cyber-Sentinel-Skills/settings/branches),
choose **Add classic branch protection rule** and target exactly `main`.
Check for existing overlapping rules before adding one. Use these settings:

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

Save the rule. If a check is absent from the selector, inspect a recent Foundation
CI run and its exact job names before saving; do not substitute an unrelated check.
GitHub documents [setup](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
and [protection behavior](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

## Review authority and verification

This initial profile enforces PRs and CI. It does not technically enforce an owner
review against another person or app with merge permission. Explicit owner merge
authorization remains mandatory under [project instructions](../../AGENTS.md).
Before adding another writer or maintainer, review the access list and adopt an
owner-approved review configuration; account for self-authored PRs before enabling
required approvals or Code Owner approval. CODEOWNERS is not an access-control list.

After setup, verify the saved settings and all four required checks on PR #1.
A public `protected: true` flag alone does not prove the required settings are
correct. Record administrative readback or owner-provided settings evidence;
do not claim deployment from this document. Do not probe by pushing to main.

If an incorrect setting blocks valid work, the administrator should correct that
specific setting after review. Record the correction; do not bypass the gate or
delete protection just to complete a merge. Repository content rollback remains
a normal revert PR. Changes to this approved profile require an owner decision.
