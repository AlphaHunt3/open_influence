# Accounts, credits and billing

As checked against the current implementation on 2026-11-23, X and Google login, shared KOL/MCP Pro access, hybrid Pro payments and permanent credit top-ups are implemented and deployed. Real OAuth and payment lifecycle acceptance remain separate from automated tests; see the account website for current provider availability and prices.

Sign in at https://mcp.xhunt.ai/account with X or a verified `@gmail.com` Google account. Create a personal API key, copy it once, and configure your agent locally. Revoking the key disables further API use. Keys are stored as hashes by the service. Browser login uses a separate HttpOnly cookie; the client does not copy it.

| Plan / login rank | Monthly allowance | Allowance daily cap |
| --- | ---: | ---: |
| XHunt 1–10,000 | 8,000 | 2,000 |
| XHunt 10,001–50,000 | 6,000 | 1,500 |
| XHunt 50,001–100,000 | 4,000 | 1,000 |
| XHunt 100,001–200,000 | 2,000 | 500 |
| Other/missing X rank or Google | 1,000 | 250 |
| Pro — price and renewal method from website | 30,000 | 7,500 |
| Approved organization | Free login allowance + approved extra 1–10,000 | floor(monthly / 4) |

X rank is refreshed on login and checked against the immutable X identity. Pro replaces the free allowance. Organization grants augment free accounts; they are not stacked on top of Pro. Used credits are retained when the plan changes. Resets use UTC calendar days/months, not a rolling 30-day purchase window.

KOL leaderboards, popular KOLs and weekly KOL lists cost 0 credits, including Pro Top500 (active Pro required). Daily hot/rising tweet API/MCP requests cost 1 credit per successful nonempty request on Free and Pro, independent of returned count. Website browsing remains free. Profiles, rank matrices and ability models cost 1 credit per successful account response. Smart Followers, Social, Circle and Profile History cost **1 credit per successful nonempty page**, including all returned groups and records, never per account/event/partner/snapshot. `limit` applies separately to each follower group or social event type; plan caps remain Free 10 / Pro 40. Cached nonempty Circle pages have the same price. Errors, empty results, pending calculations, metadata, protocol operations and usage queries cost zero credits. Data calls, including free rankings and failed admitted calls, count toward request limits; usage and discovery do not. Repeating a billable read is a new request. Rankings remain free after credit exhaustion.

Daily/monthly counters, keys and equivalent REST/MCP calls share the account’s ledger. Free allows120 requests per rolling60 seconds globally and5,000 per UTC day, with60/minute and100/day per endpoint. Pro allows300/minute globally and30,000/day, with60/minute and500/day per endpoint. Rotating keys or requesting another handle does not bypass it. Square’s alias shares the canonical endpoint counter.

Read the actual balance:

```bash
uv run influence-client usage
```

This returns `plan`, `monthly_cap`, `daily_cap`, `monthly_used`, `monthly_remaining`, `daily_used`, `daily_remaining`, `month`, `day` and `timezone`, plus permanent-wallet fields `purchased_remaining`, `available_today` and `total_remaining`. Monthly/daily fields describe allowance only; available today adds purchased credits. Both hosted MCP and this local client provide `get_usage`; REST clients can use `GET /api/v1/usage` as the official free connectivity check.

The server commits the actual result charge before releasing the data. `X-Credits-Charged` is surfaced locally as `_client.credits_charged`; a missing header is `null`. Timeouts are ambiguous: the server may already have charged. The client never retries data calls or automatically fetches a second platform.

Use the account website for named key creation/renaming/revocation, the organization application link, Checkout, top-ups and subscription management. The key list shows its prefix, UTC creation time and last recorded use. View calls shows per-key 30-day totals and latest 20 recorded requests; history starts when recording was introduced. Full keys appear only once. These are intentionally not agent data tools. Pro is granted from verified subscription state, not merely a successful redirect. The client cannot approve organizations, change plans or purchase credits.

Pro Top500 bulk access costs0 credits and retains its Pro authorization and endpoint rate policy. Local client defaults to10; hosted tool defaults to500. Both full500-row and limited-coverage responses cost0 credits. Active entitlement is checked server-side, including for internal credentials. Expiration removes access without changing historical usage. Stopping card renewal keeps access through the already-paid Pro expiry; crypto purchases have no automatic renewal to cancel.

Pro supports monthly ($19.99, list $29.90) or quarterly ($45 for three months) billing. Crypto uses Infini one-time payment; card uses Stripe automatic renewal every one or three months. Both provide 30,000 credits per month using UTC calendar-month resets; quarterly purchase does not issue 90,000 upfront. `/billing/options` includes `plans.monthly` and `plans.quarterly`; existing contracts retain their captured price and interval. Stopping renewal preserves paid access. Provider-verified orders/paid invoices grant time exactly once; redirects, pending and partial payments never grant Pro. No SDK/CLI/MCP tool purchases or cancels payments. Existing usage is not reset by payment or plan changes.

Detail, weekly and hot lists use up to 10 entries on Free or 40 on Pro per group, including profile history and weekly lists. Main ranking endpoints return up to 100 ranked accounts on either plan; the separate Pro endpoint allows up to 500. Capability discovery is metadata, not a plan-limited list. Free unfollowing/unfollowed exclude the most recent72hours and return only older timestamped events; Pro has no plan time cutoff. Following/followed are unaffected. Apply time filtering before row limits and billing; actual monitored coverage may be incomplete.

## Permanent credit top-ups

| Eligible accounts | Payment | Credits |
| --- | ---: | ---: |
| Free and Pro | $5 | 4,000 |
| Free and Pro | $10 | 10,000 |
| Free and Pro | $50 | 60,000 |
| Free and Pro | $100 | 150,000 |

Buy on the account website using crypto or card; both top-up methods are one-time payments. Purchased credits never expire, survive UTC resets and Pro expiry, and do not activate or extend Pro. Free accounts retain Free data limits after recharging. Available plan allowance is spent first, then purchased credits; the allowance daily cap does not block spending purchased credits. Endpoint rate limits still apply.

The account page shows the permanent balance, recent paid receipts and a manual refresh action. Payment verification is idempotent and uses the order’s frozen purchase terms. Automated checks and a read-only live audit have passed; actual funded top-up acceptance is still pending. No agent tool purchases credits.

Buying Pro while signed in with X also gifts the same duration of extension VIP. Every new Pro payment adds time to existing extension benefits; buying extension VIP alone does not grant website/API Pro or credits. Google purchases and credit top-ups do not include this gift. Cancelling Pro renewal does not revoke extension time already granted.

Authentication errors distinguish missing, invalid and revoked keys, wrong headers and conflicting keys. Both X-API-Key and Authorization: Bearer are supported. Data responses include `meta.billing` and `meta.freshness`; `_client.rate_limits` preserves rate-limit headers and `_client.request_id` supports call-history correlation. See [API tools](tools.md).
