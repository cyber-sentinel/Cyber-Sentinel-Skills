# Project license decision: OPEN

No project license has been explicitly approved by the owner. Foundation adds
no `LICENSE`, SPDX project-license assertion or license badge. The machine-readable
status is `pending-owner-approval`; that status is not a license.

The repository is public, but public visibility must not be treated as permission
to redistribute all content. Upstream licenses do not automatically become this
project's license. See [GitHub's licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

Original implementation may be prepared for the explicitly requested owner review.
Public release, adoption of third-party code/content and representation as a
licensed reusable distribution remain blocked pending the relevant decisions.
The packaging command creates an original-source **review-only** bundle and
includes this file; it does not settle redistribution rights or publish anything.

`python -m cskills release-check` fails closed until the owner decision is recorded
in a future reviewed change. Do not change the gate merely to make it pass.
See [ARCHITECTURE ISSUE LIC-001](docs/governance/decisions.md).
