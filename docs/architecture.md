# Architecture and security

```mermaid
flowchart LR
  A[Agent: Claude / Cursor / others] -->|Streamable HTTP + private key| H[Hosted Influence MCP]
  A -->|stdio| L[Local influence-client MCP]
  C[CLI / Python / Skill] --> R[Async REST client]
  L --> R
  R -->|HTTPS + private key| API[Influence REST API]
  H --> DATA[Shared authenticated data and credit policy]
  API --> DATA
  DATA --> X[X source caches]
  DATA --> S[Square published ranks and observed history]
  DATA --> Y[YouTube ready weekly publications]
```

The local MCP is a typed REST adapter, not a second collector or billing server. It exposes 20 tools matching the hosted set, including free get_usage via REST. It pools one async HTTP client per MCP process and performs one data request per tool call. Capability discovery uses public metadata and sends no API key.

Defaults:

- Only `https://mcp.xhunt.ai`; an explicit `XHUNT_BASE_URL` override changes where your key is sent.
- HTTPS required except loopback development. Redirects are not followed.
- Key from an argument/private environment variable, never a bundled `config.json`.
- No browser automation, raw-data downloads, filesystem writes, subprocess execution, purchases or telemetry in the runtime.
- No automatic retries, hidden pagination or paid fan-out. Main rankings default to10 and allow up to100; Pro rankings allow up to500. Optional SDK/MCP detail and hot limits use the server plan ceiling (Free10/Pro40 per group); CLI lists default to10. Limits never create hidden pagination.
- HTTP errors use safe messages; the client does not print keys, full URLs or raw upstream bodies. API payloads themselves remain untrusted external data.
- CLI JSON goes to stdout, failures to stderr. MCP owns stdout in stdio mode.
- `readOnlyHint` describes data access, not price; reads may consume credits. Retry-safety is not implied.

Review `src/influence_client/client.py`, `server.py`, `cli.py`, `pyproject.toml` and `uv.lock`. Dependencies are the official MCP Python SDK and httpx, plus their transitive dependencies. Report security concerns privately through the repository’s security advisory feature if enabled; never include a working key in an issue.

MIT applies to this client’s code. Access to the hosted service and datasets requires separate credentials and quotas. This repository contains no raw follower graphs, tweets, comments, OAuth/payment-provider secrets or server-side scoring code.
