# Verification

Updated 2026-11-23. This repository is prepared as one initial public snapshot. Verification below covers client behavior and packaging, not real payments or complete source-data coverage.

## Source checks

```bash
uv sync --locked
uv run python -m compileall -q src examples scripts
uv run python -m unittest discover -s tests -v
uv run python scripts/verify_docs.py
uv run influence-client --help
```

Offline HTTP contracts cover AI/Web3 attention and rising-tweet routing, all20 CLI operations, optional list limits, Pro validation and limited coverage, Circle pending, charge-header preservation, permanent usage fields, invalid input, safe errors and no automatic retries. Fixtures are explicitly simulated and contain no real credentials or collected user data. The documentation check validates local links/images and that all MCP tools/CLI queries appear in the reference.

## Public metadata check

```bash
uv run python scripts/verify_public_contract.py
```

This fetches only public `/openapi.json` and `/capabilities.json`, without a key. It records SDK requests against an offline transport, compares all canonical `/api/v1` GET routes and query parameters with the public schema, and checks advertised limits/prices in credits. It does not query accounts, spend credits or prove that every returned data field is correct. Current coverage:25 contract cases,19 documented paths including public capabilities; authenticated capability and Square alias routes use their canonical equivalents.

## Wheel installation

Build both artifacts freshly. `uv build` builds the wheel from the new source distribution, preventing an old same-version archive from being mistaken for current code.

```bash
uv build
uv venv dist/installed-venv --python 3.10
uv pip install --python dist/installed-venv/bin/python dist/influence_client-0.1.0-py3-none-any.whl
dist/installed-venv/bin/python scripts/verify_installed_client.py --offline
```

Run the same check for Python3.12. To verify the source distribution separately, install `dist/influence_client-0.1.0.tar.gz` into another clean environment and run the same verifier. CI covers Python3.10/3.12 × wheel/sdist; it does not publish either artifact.

The verifier rejects editable/source imports, invokes the installed CLI and SDK, and performs an actual stdio MCP initialize/list/call exchange. It verifies20 tools, Pro maximum500/default10, invalid Circle/Pro parameters and absence of removed leaderboards. Offline mode uses an empty key and loopback origin; no hosted data requests or credits are involved.

## Optional isolated data acceptance

This is separate from the offline installation gate and requires an already running isolated API and disposable personal accounts. Never seed production for this check.

```bash
export XHUNT_BASE_URL=http://127.0.0.1:18893
export XHUNT_INSTALL_TEST=1
# Privately set XHUNT_API_KEY (isolated Pro) and XHUNT_FREE_TEST_KEY.
dist/installed-venv/bin/python scripts/verify_installed_client.py
```

The script refuses other origins and requires explicit opt-in. It checks SDK, CLI and stdio rankings for all three platforms, Free denial of Pro access, actual current Web3 coverage, and0 credits charged for rankings. It no longer assumes429 channels or charges per ranking row. A successful run also checks that allowance usage and purchased balance remain unchanged. Do not run this against production accounts or describe offline fixtures as this live acceptance.

## Current evidence and boundaries

Validation repeated on 2026-11-23:

| Check | Result |
| --- | --- |
| Offline contracts, Python3.10 and3.12 | 15 passed on each interpreter |
| Local docs / images / surface coverage | 13 Markdown files,20 tools,20 CLI queries passed |
| Public OpenAPI and capabilities | 25 SDK cases, all canonical data GET paths passed; no authenticated data calls |
| Python3.10 wheel installation | CLI / SDK / actual20-tool stdio exchange passed |
| Python3.10 sdist installation | Same checks passed |
| Python3.12 wheel installation | Same checks passed |
| Python3.12 sdist installation | Same checks passed |

These results validate the client and package surfaces. Real OAuth, funded Pro/top-up payments and automatic card renewal are service acceptance work, not claims made by this client test suite. Named desktop client configurations follow standard protocols; this is not certification of every application version.

The publication snapshot is checked for credential patterns, private keys, credential-bearing database URLs and internal-only paths. Build artifacts are checked separately for accidentally bundled environment files or collected data. These checks describe their scope and are not a general security certification.

Repository visibility is controlled by the owner. After switching to Public, verify anonymous access and a clean HTTPS clone without GitHub authentication. No PyPI release, versioned GitHub release, MCP directory submission or public announcement is claimed.
