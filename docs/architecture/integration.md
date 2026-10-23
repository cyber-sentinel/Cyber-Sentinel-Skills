# Atlas, DefenseOps and interoperability boundary

Cyber Sentinel Skills owns reusable agent capabilities and their execution
contracts. It does not own Atlas canonical data, ingestion, source content packs,
deterministic search, knowledge graph or analyst workbench. It does not own
DefenseOps detection rules or Detection Forge IR.

The Foundation result envelope is a local execution result, **not a new Atlas
canonical knowledge schema**. Its simple source references identify supplied
evidence; they do not replace Atlas provenance or establish source authenticity.

A future integration may read a bounded Atlas API response or AI Context Pack,
adapt it to a Skill input and return a structured result. That adapter must retain
source identifiers and distinguish source facts, supplied assertions and generated
inferences. An independent reviewed promotion process would be needed to write
anything back into authoritative Atlas knowledge.

MCP or ordinary APIs may provide future consumer adapters. Neither is the
canonical representation of Skills or Atlas. An adapter's tool call must pass the
host's deterministic authorization before any network/write/destructive effect.
An LLM-generated approval field is not evidence of user consent.

Foundation includes no Atlas imports, source-model duplication, live data lookup,
MCP server, deployment or consequential-action adapter. This is deliberate scope,
not an integration requirement that blocks the standalone exemplars.

## Proposed consumer contract (Foundation 0.1.0)

An ATLAS or DefenseOps adapter may consume a reviewed Skill only after the host
pins the exact `contract_version`, `skill_id`, `skill_version`, and the approved
bundle identity. The adapter submits one bounded JSON input conforming to that
Skill's input schema and receives a result envelope conforming to
`schemas/result-envelope.schema.json`. It must verify the returned identity,
version, and `input_sha256` against the request before interpreting the result.
Unknown major contract versions and unknown Skill versions fail closed until
the consumer is reviewed for that version. A Skill's declared permissions are
metadata for the host to reject or accept; they are never an authorization token.

The consumer must preserve source IDs, treat source titles and URIs as untrusted
data, and display the Skill's `limitations` with its findings. No returned field
grants a write, network call, shell command, live defensive action or promotion
into ATLAS canonical knowledge. The host validates schemas and capabilities
before dispatch; a search result, document, LLM message, or manifest cannot
select a handler, path, or privilege outside the reviewed registry. This is an
interface proposal for future product adapters, not an installed integration.
