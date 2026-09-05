# Contributing

Foundation is currently an owner-led architecture review. Licensing terms for
external contributions and redistribution are not yet approved; see
[license status](LICENSE_STATUS.md). Do not add third-party source or content
under an assumed project license.

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
