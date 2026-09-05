# Security

Foundation v0.1 is experimental. It supports reviewed offline transformations of
supplied evidence, not arbitrary plugin execution or automated incident response
against live infrastructure. Read the [threat model](docs/security/threat-model.md).

For a suspected vulnerability, use the repository's GitHub **Report a
vulnerability** option if available. Its enablement has not been confirmed.
If unavailable, open a minimal issue asking the owner to establish a private
reporting channel; do not post exploit details, credentials, customer evidence or
other sensitive material in a public issue. No unverified private email address
or response-time commitment is advertised.

Include affected commit and Skill ID/version, a synthetic reproducer, observed
behavior, expected boundary and impact. Report secret exposure through a private
channel and rotate affected credentials using your organization's procedure.
The project never needs real credentials to reproduce its Foundation tests.

Never commit secrets or environment-specific evidence. The heuristic scanner is
an additional review gate, not proof that a repository or payload is secret-free.
