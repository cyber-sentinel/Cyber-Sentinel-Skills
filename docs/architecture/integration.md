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
not an integration requirement that blocks the four standalone exemplars.
