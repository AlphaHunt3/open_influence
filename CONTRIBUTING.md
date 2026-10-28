# Contributing

Useful contributions include agent research recipes, client setup corrections, translations and focused API adapter improvements. Open an issue with the use case before proposing new tools; do not advertise endpoints that the public API has not implemented.

Use Python3.10+, uv and the committed lockfile:

```bash
uv sync --locked
uv run influence-client --help
uv run influence-client capabilities
uv build
```

Keep runtime stdout reserved for MCP or CLI JSON. Never add automatic retries or hidden billable calls. Preserve source metadata, actual charged credits and unknown/null values. Avoid dependencies for features the standard library already provides. Never commit keys, cookies, account identifiers, billing data or collected datasets.

For bug reports include the command/tool, parameter values, safe error code and client/server versions. Remove secrets. Label client compatibility honestly: configuration guidance is not proof of manually testing every product version.

This initial handoff skipped test suites at the requester’s direction; see docs/verification.md for actual build/protocol verification. Future changes should include focused checks appropriate to their behavior, with isolated HTTP transports and no surprise paid requests.
