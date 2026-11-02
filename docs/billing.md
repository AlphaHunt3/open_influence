# Accounts, credits and billing

As checked on 2026-10-29, personal accounts/usage are deployed and X login is configured. New Pro purchases have moved to Infini; the payment gateway and public Influence service are deployed, with real payment acceptance still pending. Google still needs provider configuration. Pro Top500 server code is deployed; entitlement and dataset coverage must still be verified for an actual paid account.

Sign in at https://mcp.xhunt.ai/account with X or a verified `@gmail.com` Google account. Create a personal API key, copy it once, and configure your agent locally. Revoking the key disables further API use. Keys are stored as hashes by the service. Browser login uses a separate HttpOnly cookie; the client does not copy it.

| Plan / login rank | Monthly credits | Daily cap |
| --- | ---: | ---: |
| XHunt 1–10,000 | 8,000 | 2,000 |
| XHunt 10,001–50,000 | 6,000 | 1,500 |
| XHunt 50,001–100,000 | 4,000 | 1,000 |
| XHunt 100,001–200,000 | 2,000 | 500 |
| Other/missing X rank or Google | 1,000 | 250 |
| Pro — USD39/month | 30,000 | 7,500 |
| Approved organization | Free login allowance + approved extra 1–10,000 | floor(monthly / 4) |

X rank is refreshed on login and checked against the immutable X identity. Pro replaces the free allowance. Organization grants augment free accounts; they are not stacked on top of Pro. Used credits are retained when the plan changes. Resets use UTC calendar days/months, not a rolling 30-day purchase window.

All leaderboards and trending/weekly ranking lists cost0 credits, including Pro Top500 (active Pro still required). Other account data costs1 credit per returned account/event. A profile or ability model costs 1, even if it contains multiple fields/domains. Rank aggregates and profile history cost 1 per handle. Smart Followers costs the total accounts across both pools (up to 20); social costs actual events across all four types (up to 4 × limit, since limit is per type). Circle costs actual returned bilateral partners (up to10), including cached results. Other account lists cost actual returned rows, not the requested limit. Errors, empty lists, public metadata, protocol operations and usage queries cost zero credits. These still may count toward authenticated request rate limits. Repeating an account-data read is a new billable request. Rankings remain free even after the credit allowance is exhausted.

Daily/monthly counters, keys and equivalent REST/MCP calls share the account’s ledger. Each endpoint allows100 requests per rolling60 seconds per account. Rotating keys or requesting another handle does not bypass it. Square’s alias shares the canonical endpoint counter.

Read the actual balance:

```bash
uv run influence-client usage
```

This returns `plan`, `monthly_cap`, `daily_cap`, `monthly_used`, `monthly_remaining`, `daily_used`, `daily_remaining`, `month`, `day` and `timezone`. The hosted server currently has no `get_usage` MCP tool; the local client adds it via the REST endpoint.

The server commits the actual result charge before releasing the data. `X-Credits-Charged` is surfaced locally as `_client.credits_charged`; a missing header is `null`. Timeouts are ambiguous: the server may already have charged. The client never retries data calls or automatically fetches a second platform.

Use the account website for key creation/revocation, organization applications, Checkout and subscription management. These are intentionally not agent data tools. Pro is granted from verified subscription state, not merely a successful redirect. The client cannot approve organizations, change plans or purchase credits.

Pro Top500 bulk access costs0 credits and retains its Pro authorization and endpoint rate policy. Local client defaults to10; hosted tool defaults to500. Both full500-row and limited-coverage responses cost0 credits. Active entitlement is checked server-side, including for internal credentials. Expiration removes access without changing historical usage. Infini cancellation keeps access until the end of the already-paid period; an unrefreshed payment snapshot stops granting within300seconds.

Infini Pro uses USD39 monthly renewal invoices. The user pays the first checkout and subsequent invoices; do not assume automatic card charging. The website collects an invoice email, offers an explicit payment-status refresh and cancellation confirmation. A redirect or pending/partial payment never grants Pro. Only current provider-verified paid periods do; no SDK/CLI/MCP tool creates or cancels payments. Existing usage is never reset by a plan change.
