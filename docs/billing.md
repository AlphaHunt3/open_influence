# Accounts, credits and billing

This document describes the implementation in the auth-billing worktree. Actual login providers and Stripe purchases require deployment and provider credentials; it is not a claim that a real payment has been verified.

Sign in at https://mcp.xhunt.ai/account with X or a verified `@gmail.com` Google account. Create a personal API key, copy it once, and configure your agent locally. Revoking the key disables further API use. Keys are stored as hashes by the service. Browser login uses a separate HttpOnly cookie; the client does not copy it.

| Plan / login rank | Monthly credits | Daily cap |
| --- | ---: | ---: |
| XHunt 1–10,000 | 8,000 | 2,000 |
| XHunt 10,001–50,000 | 6,000 | 1,500 |
| XHunt 50,001–100,000 | 4,000 | 1,000 |
| XHunt 100,001–200,000 | 2,000 | 500 |
| Other/missing X rank or Gmail | 1,000 | 250 |
| Pro — USD39/month | 30,000 | 7,500 |
| Approved organization | Free login allowance + approved extra 1–10,000 | floor(monthly / 4) |

X rank is refreshed on login and checked against the immutable X identity. Pro replaces the free allowance. Organization grants augment free accounts; they are not stacked on top of Pro. Used credits are retained when the plan changes. Resets use UTC calendar days/months, not a rolling 30-day purchase window.

One successfully returned account/channel costs 1 credit. A profile or ability model costs 1, even if it contains multiple fields/domains. Lists cost actual returned rows, not the requested limit. Errors, empty lists, public metadata, protocol operations and usage queries cost zero credits. These still may count toward authenticated request rate limits. Repeating a read is a new billable request.

Daily/monthly counters, keys and equivalent REST/MCP calls share the account’s ledger. Each endpoint allows100 requests per rolling60 seconds per account. Rotating keys or requesting another handle does not bypass it. Square’s alias shares the canonical endpoint counter.

Read the actual balance:

```bash
uv run influence-client usage
```

This returns `plan`, `monthly_cap`, `daily_cap`, `monthly_used`, `monthly_remaining`, `daily_used`, `daily_remaining`, `month`, `day` and `timezone`. The hosted server currently has no `get_usage` MCP tool; the local client adds it via the REST endpoint.

The server commits the actual result charge before releasing the data. `X-Credits-Charged` is surfaced locally as `_client.credits_charged`; a missing header is `null`. Timeouts are ambiguous: the server may already have charged. The client never retries data calls or automatically fetches a second platform.

Use the account website for key creation/revocation, organization applications, Checkout and subscription management. These are intentionally not agent data tools. Pro is granted from verified subscription state, not merely a successful redirect. The client cannot approve organizations, change plans or purchase credits.
