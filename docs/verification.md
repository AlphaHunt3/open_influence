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
