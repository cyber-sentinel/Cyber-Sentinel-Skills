# Foundation threat model and enforcement

## Assets, inputs and trust

Assets are analyst evidence, host resources, source provenance, reproducible
results and repository integrity. Untrusted material includes input JSON, source
URLs, source text, supplied claims, model output and proposed manifest changes.
The trusted computing base is the reviewed host package, its pinned dependencies,
registered handlers and deployment environment. An attacker who can modify that
Python code can change the policy; a JSON contract is not an OS sandbox.

The host loads contract/schema files from its reviewed checkout. The CLI takes a
caller-selected workspace and a relative JSON input file. Handlers receive a
detached in-memory payload and return data. They never receive an open file,
network client, model client, shell, environment lookup or arbitrary callable.

## Capability enforcement

| Class/resource | Foundation behavior | Future requirement |
|---|---|---|
| READ | Analyze supplied JSON values; host reads only selected input and installed metadata | Mediate any new external evidence acquisition |
| ANALYZE | Registered pure transformation | Declare new runtime/data dependencies |
| GENERATE | Return structured JSON in memory; CLI writes result to stdout | Review output destinations and sensitivity |
| WRITE | Rejected for every Skill | Bounded destination, explicit effects and trusted authorization |
| EXECUTE | Arbitrary commands/tools rejected | Reviewed executable adapter, isolation and deterministic argument policy |
| DESTRUCTIVE | Rejected, even with claimed approval | Explicit user authorization and separately approved execution/rollback design |
| Network / hosts | All network capability requests rejected | Exact host/port/protocol scope, redirect/DNS/private-address policy and egress mediation |
| Filesystem / environment | No handler access; caller's explicit input scope is handled separately | Bounded handles and protection against concurrent path replacement |
| Models / services | None required or called | Data exposure decision and declared nondeterminism |

The host's fixed authorization decision is made after manifest validation and
before handler dispatch. An unknown field, missing manifest, unsupported contract,
unregistered handler, unexpected tool, service, side effect or permission fails
closed. User approval strings are neither accepted in input schemas nor used as
authorization. Foundation has no implementation for consequential actions, so
even genuine approval requires a future reviewed adapter rather than a flag here.

## Threats and controls

| Threat | Implemented control | Limit |
|---|---|---|
| Prompt injection in evidence | Evidence remains data; no dynamic dispatch or evaluation from text | Downstream agents/renderers must preserve the data/instruction boundary |
| Manifest permission escalation | Exact fixed profile plus registered handler binding | Host source modification is outside this policy's protection |
| JSON ambiguity / oversized evidence | Duplicate keys, NaN/Infinity, invalid JSON, excessive depth and byte size rejected | No general-purpose adversarial schema sandbox |
| Schema-driven SSRF / file reads | External and nonlocal references rejected; retrieval disabled | Reviewed schemas are part of the trusted checkout |
| Path traversal / symlink escape | Absolute paths, traversal, alternate separators and symlink components rejected | Selected roots must not be concurrently attacker-writable; no claim of TOCTOU-safe OS isolation |
| Secret disclosure | Secret-like fields/values rejected; errors omit payloads; no evidence logging | Heuristics cannot identify every unknown or encoded secret; outputs can retain legitimate sensitive evidence |
| Misleading evidence conclusions | Sources retained; fact/inference labels preserved; limitations explicit | References and hashes do not establish source truth |
| Tampered review bundle | Exact member set, safe regular paths and SHA-256 file inventory checked | Checksums are not signatures or proof of publisher identity |
| Undeclared code/tool surface | Skill file inventory and handler AST import/primitive gate | Static inspection complements review and is not proof for arbitrary Python |
| CI credential abuse | Read-only token scope, no project secrets, no persisted checkout credential, pinned actions | Repository settings must enforce reviews and required checks |

## Operational use and rollback

Begin with the committed synthetic examples in an isolated development checkout.
No test contacts production targets, consumes real customer logs or performs an
incident-response action. The only CLI mutation is creating an explicitly named,
new review ZIP; existing files are never overwritten. Delete that newly created
review ZIP to undo the packaging operation. Skills themselves create no files.

Before processing real evidence, the host owner must protect input/output storage
and restrict access to the resulting JSON. Do not mistake secret heuristics for
an approved data-loss prevention system. Do not place raw output directly into
HTML, a shell command or an agent instruction message.

For a defective future merged change, prepare a normal revert PR and rerun the
same gates. Do not force-reset `main`. An unmerged proposal can be closed without
changing the main branch. No deployment or production rollback is part of v0.1.

## Validation scope

CI validates the contract, metadata, stable ID uniqueness, SemVer, file inventory,
declared dependencies, fixed policy, known secret surfaces, synthetic expected
results, relative documentation file links, pinned workflow actions and packaging.
Tests cover negative cases, deterministic output, isolated bundle execution,
tampering and error redaction. Local link checks do not establish external URL
availability or heading-anchor correctness. The scanner is heuristic and the AST
gate is deliberately specific to the fixed handlers.

Linux and Windows with Python 3.11/3.12 are the CI matrix. macOS is an intended
portable Python host but is not CI-certified in Foundation. Windows symlink tests
exercise actual links when the runner permits creating them; other path rejection
cases run on every platform.
