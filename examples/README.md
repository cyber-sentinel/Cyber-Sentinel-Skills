# Running the original exemplars

All examples contain synthetic evidence and non-live reference identifiers. Run
from an isolated, reviewed repository checkout after installing `requirements.txt`.
Each command prints a JSON envelope; none contacts a target or external source.

```bash
python -m cskills run cs.skills.research.summarize-evidence --workspace skills/research/summarize-evidence/examples --input input.json
python -m cskills run cs.skills.threat-intelligence.normalize-iocs --workspace skills/threat-intelligence/normalize-iocs/examples --input input.json
python -m cskills run cs.skills.incident-response.build-timeline --workspace skills/incident-response/build-timeline/examples --input input.json
python -m cskills run cs.skills.detection-engineering.review-detection-spec --workspace skills/detection-engineering/review-detection-spec/examples --input input.json
```

The envelope contains contract/Skill versions, stable Skill ID, determinism,
canonical input SHA-256, supplied source references and a Skill-specific result.
The committed `expected.json` files assert the `result` value only; envelope
behavior, digests, references and isolation are tested separately.

Exit code 0 means the transformation completed and its output matched its schema.
It does not certify maliciousness, incident causation, source authenticity or
query correctness. Exit code 2 means the host rejected input/policy or could not
perform its explicit file operation; error JSON does not echo the payload.

To process a different synthetic input, place it inside a directory selected with
`--workspace`, then name the file relative to that directory with `--input`.
Absolute input paths, traversal and symlink components are rejected. Keep the
directory private and stable during execution. Never paste secrets into examples.

On Windows, if virtualenv activation is restricted, invoke
`.venv\Scripts\python.exe` directly in place of `python`; no global execution-policy
change is needed. The core does not require administrator privileges.

See the [authoring contract](../docs/skill-authoring/contract.md) and
[security model](../docs/security/threat-model.md) before embedding the Python API.
