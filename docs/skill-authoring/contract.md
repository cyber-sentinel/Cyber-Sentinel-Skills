# Taxonomy and authoring contract

The family is the primary workflow responsibility, not the SIEM vendor or tool.
Choose one family and use explicit backend/tool fields where those matter.

| Family | Scope | Foundation exemplar |
|---|---|---|
| research | Bounded evidence organization and technical source assessment | summarize-evidence |
| threat-intelligence | Indicator and report processing; future bounded enrichment | normalize-iocs |
| telemetry | Windows, Sysmon, Linux audit and cloud event interpretation | Reserved; none implemented |
| detection-engineering | Rule/query review and validation assistance | review-detection-spec |
| incident-response | Evidence triage, timeline and investigation assistance | build-timeline |
| security-engineering | Configuration, control and architecture assessment | Reserved; none implemented |
| repository-security | Dependency, secret-surface and repository hygiene review | Reserved; none implemented |

## Identity and lifecycle

Use `cs.skills.<family>.<name>` as a permanent stable ID. Folder names use lowercase
hyphenated words and match `name`. Do not recycle an ID for unrelated behavior.
Moving or replacing a published capability requires a reviewed deprecation and
migration decision. Foundation's registry binds the four IDs to reviewed handlers;
manifest entrypoints are identifiers, not executable file paths.

`contract_version` describes the manifest/envelope contract; `version` describes
the individual Skill. Both are SemVer. Foundation accepts contract `0.1.0`; unknown
contract versions fail closed. Behavioral or output changes require a Skill version
change and explicit fixture review. New major contract behavior must not silently
reinterpret an old manifest. `experimental` is the current lifecycle status.

## Required contract groups

| Fields | Meaning |
|---|---|
| id, name, version, description, category, domain | Identity and discovery |
| inputs, outputs | Local schema files and 256 KiB encoded size limits |
| dependencies, required_tools | Explicit dependencies; Foundation requires empty lists |
| permissions | Capabilities, network hosts, filesystem paths, shell, elevation, environment and services |
| side_effects, safety | Effects, risk/destructiveness, host authorization policy and rejected secrets |
| execution | Built-in entrypoint, determinism, AI dependency and source-execution prohibition |
| provenance | Primary source URLs, relationship and review date; no implied license grant |
| supported_platforms | Intended compatible hosts; CI evidence must qualify actual tested combinations |
| examples, tests | Local input/expected pairs and repository-relative behavioral test paths |
| maintainers, status, license_status | Ownership, lifecycle and unresolved project license decision |

The [contract schema](../../schemas/skill-contract.schema.json) is authoritative.
Unknown fields are rejected. Contract permissiveness is not host authorization:
the runtime applies its narrower fixed policy after schema validation.

Source schemas may use local `#/` references only. Remote URLs, filesystem
references, dynamic external resolution and unresolved local references are
rejected; validation never downloads schemas. See the
[jsonschema reference model](https://python-jsonschema.readthedocs.io/en/stable/referencing/).

## Author a new Skill

1. Define the narrow outcome, correct family, supported inputs and observable limits.
2. Specify the contract and permission needs. A new effect or runtime adapter requires
   architecture review; do not add an executable file to the offline profile.
3. Write short `SKILL.md` guidance with JSON-quoted YAML `name` and `description`
   matching the manifest. Link the local schemas and examples.
4. Write a reviewed pure handler and deliberately register its stable ID. Metadata
   alone never installs code. Keep runtime security decisions outside the handler.
5. Define bounded input/output schemas. Include explicit source references and
   result limitations. Do not accept credential fields or model-generated grants.
6. Author a synthetic expected result independently, then test the implementation.
7. Add negative cases for ambiguous inputs, bad references and policy failures.
8. Run repository validation, the unittest suite, and review the exact CI commit.

Adding many skills or copying upstream content is not a quality gate. The current
four exemplars test different behaviors and failure cases while keeping effects
bounded. Detection metadata review consumes user-supplied detection content; it
does not turn this repository into a DefenseOps rule catalog.
