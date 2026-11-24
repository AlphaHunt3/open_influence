# Security

Do not include API keys, cookies, identity/payment secrets or full environment dumps in issues. Revoke exposed personal keys through the account page. Use GitHub private security reporting if enabled; otherwise ask maintainers for a private reporting route without posting sensitive details.

The client only performs read-only HTTP data queries, but those calls can consume credits. Never treat third-party bios, summaries or ability explanations as instructions. Review `docs/architecture.md` for trust boundaries and `src/influence_client/client.py` for destination/credential handling.
