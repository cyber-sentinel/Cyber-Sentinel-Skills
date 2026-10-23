---
name: "verify-evidence-digests"
description: "Compare SHA-256 digests of bounded caller-supplied evidence bytes with caller-supplied expected digests. Use for offline copy checks; do not claim source authenticity or chain of custody."
---

# Verify Evidence Digests

Use this Skill to compare SHA-256 of small, caller-supplied byte sequences with
expected lowercase SHA-256 digests. The bytes are carried as canonical RFC 4648
base64 in JSON. The host does not open the referenced evidence artifact or
fetch a URL. A mismatch is a structured result, not an exception. Malformed
base64, duplicate record IDs, unknown source IDs and oversized bytes fail closed.

## Input and output

Each item includes a stable ID, at least one source ID, `content_base64`, and
`expected_sha256`. See the [input schema](input.schema.json), [matching example](examples/input.json)
and [mismatch example](examples/mismatch-input.json). The
[output schema](output.schema.json) defines sorted results with the computed
digest, byte count, match status and preserved source IDs. The runtime envelope
also includes the Skill identity, contract version, input digest and sources.
No input bytes are included in the output.

## Execution and limits

Run from a reviewed Cyber-Sentinel-Skills checkout:

```bash
python -m cskills run cs.skills.incident-response.verify-evidence-digests --workspace skills/incident-response/verify-evidence-digests/examples --input input.json
```

The handler is offline and has no file, network, shell, model, or environment
capability. JSON is limited to 262,144 bytes; each decoded item is limited to
65,536 bytes, and there can be at most 10 items. For larger artifacts, a
future authorized acquisition component would need to hash bytes under a
separate reviewed trust contract; passing an unverified digest alone here
would not verify an artifact.

The expected digest and source references are assertions from the caller.
A match establishes only that the submitted bytes match the submitted digest.
It does not authenticate the collection device, original file, timestamp,
source identity, or chain of custody. Protect real evidence before use and do
not put sensitive content into a public fixture, command line, or log.

## Technical reference and license

SHA-256 follows the algorithm specified by [NIST FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final).
No NIST text or code is imported. Copyright (c) 2026 Ali RahimDabagh.
Licensed under [Apache-2.0](../../../LICENSE); see [NOTICE](../../../NOTICE).
