# Tool and API reference

Contract updated 2026-11-06. Check capabilities for current data coverage and provider availability. Local stdio exposes20 tools:19 hosted data/discovery tools plus `get_usage` (REST wrapper).

Main influence limits: Free100/Pro500. Per-group detail/hot limits: Free10/Pro40. All weekly lists and profile history: Free10/Pro40. Optional detail/weekly/hot limits omitted use the server-verified plan maximum; larger requests are clamped, smaller requests respected. Main local rankings default10 for response size; hosted main rankings default100, Pro500. Social client maximum100, effective plan cap10/40 per event type.

| Local / hosted MCP tool | REST GET | Parameters | Credits |
| --- | --- | --- | ---: |
| `get_capabilities` | `/capabilities.json` (public), `/api/v1/capabilities` (key) | none | 0 |
| `get_usage` **local only** | `/api/v1/usage` | none | 0 |
| `get_leaderboard` | `/api/v1/leaderboards/influence` | sector, region, limit; kind=influence | 0 |
| `get_leaderboard` | `/api/v1/leaderboards/weekly-growth` | sector, region, limit; kind=weekly_growth | 0 |
| `get_pro_leaderboard` | `/api/v1/pro/leaderboards/{platform}` | platform=x/binance-square/youtube, sector, region (X only), limit | 0; active Pro required |
| `get_kol_profile` | `/api/v1/kols/{handle}` | X handle | 1 |
| `get_kol_ranks` | `/api/v1/kols/{handle}/ranks` | handle | 1 |
| `get_smart_followers` | `/api/v1/kols/{handle}/smart-followers` | handle, sector, limit | actual accounts across both pools, Free up to20 / Pro up to80 |
| `get_kol_social` | `/api/v1/kols/{handle}/social` | handle, limit **per type** | actual events across four types, up to 4 × limit |
| `get_kol_circle` | `/api/v1/kols/{handle}/circle` | handle, days=7 (1–30), limit | actual partners, Free10/Pro40 |
| `get_profile_history` | `/api/v1/kols/{handle}/profile-history` | handle, limit | 1 per handle |
| `get_ability_model` | `/api/v1/kols/{handle}/abilities` | handle, sector, limit | 1 |
| `get_weekly_kols` | `/api/v1/weekly/kols` | sector, region, mode, limit | 0 |
| `get_binance_square_leaderboard` | `/api/v1/binance-square/leaderboard` | limit | 0 |
| `get_binance_square_profile` | `/api/v1/binance-square/kols/{square_uid}` | immutable UID | 1 |
| `get_binance_square_abilities` | `/api/v1/binance-square/kols/{square_uid}/abilities` | immutable UID | 1 |
| `get_binance_square_weekly_trending` | `/api/v1/binance-square/weekly/trending` | metric, limit, region | 0 |
| `get_youtube_leaderboard` | `/api/v1/youtube/leaderboard` | sector, limit | 0 |

| `get_hot_kols` | `/api/v1/trending/hot-kols` | sector, cn/en region, days=1 or 7, optional limit | 0 |
| `get_hot_tweets` | `/api/v1/trending/hot-tweets` | sector, cn/en region, optional limit | 1 per successful nonempty request, Free and Pro |
| `get_rising_tweets` | `/api/v1/trending/rising-tweets` | web3 sector, cn/en region, optional limit | 1 per successful nonempty request, Free and Pro |

Popular KOLs preserve existing engagement ranks: days=1 daily (Free10/Pro40), days=7 weekly (Free10/Pro40); popular tweets preserve the24-hour source score. Rising tweets preserve the existing age-calibrated observed view-velocity rank, Web3 only. Source shortages remain visible; the current rising pool may supply20, not40. Published ability models currently do not attach tweets; attached tweet groups, if supplied, follow10/40. History is newest first.

The existing Square alias `/api/v1/leaderboards/binance-square` shares billing/rate counters with the canonical route. Sector is `ai` or `web3`; X region is `global`, `en` or `cn`. X handles accept an optional leading `@` in the client. Square UIDs come from leaderboard rows; they are not usernames or X handles.

## Weekly definitions

| Feature | Exact meaning | Restrictions |
| --- | --- | --- |
| X `kind=weekly_growth` | Previous rank minus current rank over approximately seven days | AI/Web3, global/en/cn; inspect actual available count |
| X `mode=attention` | New attention from the monitored KOL network | Web3 only, cn/en only; not raw follower-count growth |
| X `mode=new_entries` | Current Top200 minus a comparable seven-day baseline | Includes re-entries; returns insufficient_history until a baseline exists |
| Square `metric=followers` | Absolute net total follower gain over seven days | Current influence Top1000; requires measured counts at both ends |
| Square `metric=smart_followers` | Absolute net gain in monitored source accounts following the KOL | Same candidate pool; source pool must be comparable |

Square weekly `region=global|en|cn` filters published account language **before** sorting and limiting within the current global influence Top1000. English includes `en-*`, Chinese includes `cn`/`zh`/`zh-*`; unknown tags remain global-only. This parameter is added in the 2026-10-29 source changes and requires deployment; verify `weekly_regions` in capabilities before using a language-specific list. An older server may ignore the new parameter. `available_count` reports eligible growth rows before limiting, and `influence_rank` preserves global influence rank.

Do not label attention as follower growth or new entries as “first discovered.” Square weekly history began on 2026-10-28; a usable seven-day baseline is expected around 2026-11-04, subject to successful collection and comparable observations. Missing counts remain unknown.

## Ranking and abilities

- X: person-filtered influence source. `global` combines source pools; `en` maps to the international pool. Do not claim strict English-only coverage. The profile is normalized and limited to available fields.
- Square: fixed Top200 sources, following contribution divided by `max(actual following,20)`, 10% quotes, then support breadth discount. The discount reduces influence supported by only a few sources; it is not a probability or a fraud verdict. High-following accounts may remain ranking targets even when their following behavior is excluded as a source.
- YouTube: original `yt_weekly_v2` scores; `web3` maps to Crypto. Lists include public subscribers and basic metrics. Preserve `week_id`, `method_ver`, `source_updated_at` and collection window. The publisher consumes ready reports, not live video search.
- X/Square abilities: only scores >=85; an empty published list is valid. No soul index, ability leaderboard or soul leaderboard is offered.

Scores across platforms have different definitions. Combine shortlists, not scores; a cross-platform identity match needs independent verification.

## Responses and errors

Lists preserve `{items, meta}` plus optional `status`/`reason`. Profiles/models use `{data, meta}`. The local client adds `_client.credits_charged`; `null` means the header was absent, not free.

- `available`: data is returned for this publication. Read actual timestamps.
- `insufficient_history`: wait for a comparable baseline; do not invent rows.
- `stale_data`: observation window is too old.
- 401: key absent, invalid or revoked.
- 404: account/model absent, or endpoint not deployed.
- 422: invalid or unsupported parameters.
- 429 `rate_limited`: per-endpoint request rate exceeded. Respect Retry-After.
- 429 `quota_exceeded`: daily or monthly credit cap. A short retry does not restore credits.
- 5xx: source/service failure. Data requests are not automatically retried.

## Coverage boundaries

X profiles include recorded current profile fields and known person/project and Chinese/international classifications. Six-rank aggregates include project ranks when available, with population counts from fresh completed source cohorts when configured (`kol_count_scope=ranked_accounts_including_projects`). Missing/stale snapshots remain `kol_count=null`; inspect `kol_count_status` and timestamps. This publisher requires separate deployment/configuration. Smart Followers preserves the source ordering, at most 10 per global/cn pool per sector, with unknown classifications left null. International classification does not verify English language.

Social covers monitored following, followed, unfollowing and unfollowed events. The limit is per event type, not a time window. Unfollows cover approximately the last hour; follow records use the source's recent-observation filter. Missing arrays are unavailable, not evidence of no activity. Profile history is recorded snapshots in source order, not lifetime coverage or inferred effective change times.

A complete Following KOLs list, raw timelines/tweet search and cross-platform identity matching remain unavailable.

There are no YouTube profile/ability or real-time streaming endpoints in this contract. Data cadence is not an uptime or freshness guarantee; capabilities and metadata take precedence.

Circle requires the candidate backend with an explicitly configured read-only post source. It measures observed bilateral replies/quotes/reposts: at least one action each way, sorted by total unique posts, minimum directional count, then ID. Missing target posts give `partial`; this is monitored coverage and unknown ingestion freshness, never complete X activity. Query caps fail instead of silently truncating results. Production availability is deployment-dependent; inspect capabilities.

Pro uses a server-verified active entitlement. Local default10, hosted default500; ordinary endpoints stay capped at100. Free, canceled or expired accounts receive pro_required; internal credentials alone do not grant Pro. YouTube uses verified eligible pool_rank values, never re-sorts or relaxes eligibility. Inspect insufficient_coverage, available_count and source dates; the archived W44 source supports AI500 but only429 Web3 ranks. Production availability and wallet-account linking are separate deployment/work items.

Free unfollowing and unfollowed events must be older than 72 hours. Pro has no plan time cutoff, subject to available confirmed records. Following and followed events have no additional plan time restriction.

Circle caches source snapshots durably and refreshes active accounts in the background. Inspect `meta.cache_state`, `cache_computed_at`, `cache_age_seconds` and `refresh_status`. After5 minutes an available snapshot is explicitly `status=stale_data`, with its original coverage status in `meta.snapshot_status`; after1 hour it cannot be served without successful recomputation. Cached returned accounts retain normal per-account billing. Only confirmed SQL statement timeouts with a working durable cache return `status=pending` (REST HTTP202, `Retry-After`); retry the same request after `meta.retry_after_seconds`. Pending responses have no rows and cost0 credits. The server bounds retries and the pending window; terminal timeout and other source failures remain errors, not successful examples. Results retain normal per-account billing.
