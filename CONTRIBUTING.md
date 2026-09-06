# Contributing

Foundation is currently an owner-led architecture review. Original project code,
Skills and documentation are licensed under [Apache-2.0](LICENSE); see the recorded
[owner decision](LICENSE_STATUS.md). Contributions intentionally submitted for
inclusion follow section 5 of that license unless explicitly stated otherwise.
Disclose any different terms before review. Do not add third-party source or
content under an assumed license or claim rights you do not have.

## Who decides what enters the project

The canonical project is maintained by `@cyber-sentinel`. The owner decides the
roadmap, scope, architecture and acceptance of contributions. Submitting an issue
or PR does not grant write access, merge authority or a right to acceptance.
Contributions may be declined when they do not fit the approved direction, even
when their tests pass. A fork is a separate project; changes there do not change
this repository.

Before implementing a new feature, capability family, integration or architectural
change, open a focused proposal describing the problem, scope, alternatives,
security impact and validation plan. Wait for the owner's scope decision. Small
bug fixes and documentation corrections may be proposed directly in a focused PR;
they still require review and explicit owner merge authorization.

Preserve source attribution and provenance. Disclose upstream material and its
exact revision and license; do not present third-party work as original work.
Credit accepted contributors accurately. Apache-2.0 governs reuse rights; these
contribution rules govern acceptance into the canonical repository and do not add
restrictions to the license. Preserve applicable notices, including [NOTICE](NOTICE).

Keep contributor access separate from accepting a contribution. Adding anyone
with write, maintain or admin access requires an owner decision and review of the
[main protection profile](docs/governance/main-protection.md). CODEOWNERS alone
does not enforce review or prevent merging.

## Contribution workflow

1. Read latest `main`, open branches and the [architecture decision](docs/architecture/0001-foundation.md).
2. Create a focused feature branch from latest `main`.
3. Propose taxonomy and contract changes before introducing new capability classes.
4. Implement original code and small, explicit Skills. Preserve stable IDs and
   record source references. Follow the [authoring contract](docs/skill-authoring/contract.md).
5. Add meaningful positive and fail-closed tests; expected fixtures must be reviewed
   independently of the handler implementation. No live targets or credentials.
6. Run catalog validation and the unittest suite. Inspect the complete diff,
   especially handlers, runtime policy, dependencies, manifests and workflows.
7. Push the feature branch, inspect CI at its exact SHA and open a PR with evidence.
8. Await explicit owner approval to merge. A green CI run is not merge approval.

Report base `main` SHA, branch, head SHA, changed files, tests, CI run links, open
architecture issues, license status and merge readiness. Never repair a routine
test failure by weakening a policy boundary or bypassing a required gate.

Use `READ`, `ANALYZE`, `GENERATE`, `WRITE`, `EXECUTE` and `DESTRUCTIVE` precisely.
Adding an external service, shell handler, write path or destructive operation
changes the security boundary and requires a separate reviewed design. An
approval-looking string inside a test input cannot authorize anything.
