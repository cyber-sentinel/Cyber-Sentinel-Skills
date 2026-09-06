# Project license decision: APPROVED

On 2026-09-06 Ali RahimDabagh (`@cyber-sentinel`) explicitly approved unmodified
**Apache-2.0** for the project's original code, Skills and documentation, together
with project attribution in [NOTICE](NOTICE). The complete terms are in
[LICENSE](LICENSE). This resolves [LIC-001](docs/governance/decisions.md).

Copyright (c) 2026 Ali RahimDabagh.
Canonical source: [Cyber-Sentinel-Skills](https://github.com/cyber-sentinel/Cyber-Sentinel-Skills).

The license text was retrieved from the
[Apache Software Foundation](https://www.apache.org/licenses/LICENSE-2.0.txt)
on 2026-09-06 without changing its terms. Its LF-normalized SHA-256 is
`cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.
NOTICE identifies the original project and author; it adds no license conditions.
The [contribution rules](CONTRIBUTING.md) control acceptance into this repository.

Skill and bundle manifests declare `license_status: approved` and
`license: Apache-2.0`. Repository validation and bundle verification require the
approved LICENSE text and the project attribution in NOTICE. These checks are
offline consistency gates, not proof of authorship, an authenticity signature or
a substitute for reviewing third-party rights.

User-supplied evidence and separately identified third-party material retain their
own rights. Referenced projects and installed dependencies are not relicensed by
this decision. No upstream Skill or implementation has been imported, and review
bundles do not vendor dependencies. Retain the relevant license and attribution
materials when distributing the project or individual Skills under the license.

The packaging command still creates an experimental **review-only** source bundle.
That label describes its release lifecycle; the contents are licensed as above.
It does not publish anything. `python -m cskills release-check` first validates
the source, then returns exit code 2 with `release-owner-approval-pending` because
an official project release has not been authorized. License approval does not
grant release authority. The existing conditional merge approval remains recorded
in [governance decisions](docs/governance/decisions.md).
