# Verification record

Prepared2026-10-28. Test suites were skipped at the requester’s direction.

Completed locally:

- Resolved and locked dependencies with uv0.10.0 on Python3.12.3.
- Compiled client/example Python sources and built both sdist and wheel successfully.
- Imported the MCP server and ran the CLI help command.
- Ran the real stdio MCP handshake through the official SDK:11 tools discovered, all5 list tools expose default10 and bounds1–200.
- Called the local MCP capability tool against the public HTTPS service: X, Binance Square and YouTube were available. The current service omitted a credit header; the client preserved `null` rather than asserting free billing for data calls.
- Verified missing-key usage is a tool error without a credentialed request.
- Checked relative Markdown links.

No data query, login, Stripe payment or paid call was performed for this client verification. Personal account/billing endpoints in the auth-billing worktree are documented from source and are not claimed to be deployed by this repository. The client does not deploy or modify that service.

Hosted REST/MCP and Chinese/English desktop/mobile website behavior were separately checked during the preceding platform integration. The included website screenshot comes from that real2026-W44 YouTube view; it is not output fabricated by this client.

Client configuration examples target standard Streamable HTTP or stdio. Claude Desktop, Cursor, Windsurf and VS Code application UIs were not all manually exercised, so they are documented configurations rather than a broad certified compatibility claim. No PyPI release, remote GitHub repository, directory submission or launch post is claimed.

## Contract sync — 2026-10-29

Added the four deployed X per-handle APIs to SDK, CLI and local MCP. The earlier 11-tool verification above is historical; current discovery exposes 15 tools. Coverage/billing documentation now reflects the deployed account service, with Gmail and payments still disabled.

Validation: `PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v` (3 passing checks, HTTP mocked): malformed inputs fail before a billable request; unknown fields/coverage and actual charge survive SDK handling; MCP discovers the new tools and bounds social limits per type. CLI help and Python compilation also checked. No real payment or new client-app certification is claimed.

2026-10-29 Circle client addition: local discovery now16 tools (15 hosted plus usage); SDK, CLI and MCP support days1–30/default7. Five mocked HTTP/contract tests passed, including Circle invalid-window rejection before requests, coverage/credit preservation, and MCP window schema. Source and deployment verification belongs to the backend progress record.

Pro addition: local discovery17 tools (16 hosted plus usage). Six contract checks pass; Pro invalid parameters fail before a request, limit500 is forwarded, the local default is10, and429-row insufficient_coverage/credits survive unchanged. These mocked checks do not certify production payment or wallet linking.

## Wheel installation

A checkout test can pass even if the distributable has a broken entrypoint or missing files. Build a wheel, install it in a separate environment and test that installation:

```sh
uv build --wheel
uv venv dist/installed-venv --python 3.10
uv pip install --python dist/installed-venv/bin/python dist/*.whl
dist/installed-venv/bin/python scripts/verify_installed_client.py --offline
```

The script rejects imports outside the interpreter's prefix. The offline variant sets an empty key and loopback base URL, checks CLI help, the SDK's missing-key behavior and a real stdio MCP initialize/list/call exchange. It verifies17 tools, no removed ability/Soul leaderboard tools, Pro default10/max500 and invalid Circle/Pro limits. No data requests or credits are used. The GitHub workflow runs this after building; it does not publish a package.

For actual service verification, use an isolated API on **127.0.0.1:18893**, a personal Pro key and a separate free personal key from its isolated database. Do not use an internal bypass key, production account or real subscription. Set secrets privately in the process environment:

```sh
export XHUNT_BASE_URL=http://127.0.0.1:18893
export XHUNT_INSTALL_TEST=1
# Privately configure XHUNT_API_KEY and XHUNT_FREE_TEST_KEY, then:
dist/installed-venv/bin/python scripts/verify_installed_client.py
```

This version refuses other API origins and requires explicit test opt-in. It makes actual SDK, CLI and stdio tool calls: one YouTube SDK row, one CLI Pro row, X/Square/YouTube one row each and the W44 YouTube Web3 pool429. It checks `X-Credits-Charged`, shared monthly usage increasing by434, free-key Pro403 with unchanged free usage, public discovery/usage free and invalid limits rejected. It has no retries. The429 expectation deliberately anchors the current W44 test dataset; update the verifier and evidence when an independently verified real dataset changes coverage.

On2026-10-29 a fresh wheel environment (Python3.12, resolved mcp1.30.0) passed offline and isolated-live verification with17 tools and434 actual test credits. The six existing offline contract tests also remain separate checks. This proves local wheel/stdio installation against the isolated candidate, not public PyPI availability, GitHub publication or a named desktop agent UI. The configured remote still needs restored access before public delivery; do not advertise a release as published.


## Minimum Python and source-distribution acceptance — 2026-10-29

The package advertises Python >=3.10. Python3.10.19 now passes the six offline contracts using `uv sync --locked` in a separate environment. Its independent wheel installation also passes the actual CLI/SDK/stdio offline verifier:17 tools, valid schema limits and0 data credits.

An archive-to-source comparison found that the existing local `.tar.gz` still contained older client/CLI/MCP sources and documentation, while the wheel matched current sources. Nothing was published. Rebuild **both** artifacts with `uv build`, rather than treating an old same-version archive as the current release. This command builds the wheel from the newly generated source distribution.

Fresh source-distribution installations on Python3.10.19 and3.12.3 both pass the same independent offline verifier. Installation resolves the dependencies allowed by each interpreter (mcp1.30.0 in both); it is deliberately separate from the locked source-contract environment. The package workflow now covers Python3.10/3.12 × wheel/sdist, building fresh artifacts in each job. GitHub execution is still pending repository access; local results do not assert remote CI success.

To check the source distribution separately:

```sh
uv build
uv venv dist/installed-sdist-venv --python 3.10
uv pip install --python dist/installed-sdist-venv/bin/python dist/influence_client-0.1.0.tar.gz
dist/installed-sdist-venv/bin/python scripts/verify_installed_client.py --offline
```

The current artifacts contain the MIT license and have been inspected for matching package sources. These checks make no public release, real OAuth, payment, data-call or named desktop-app certification claim. Restore the intended GitHub remote/access before publishing or announcing an install channel.
