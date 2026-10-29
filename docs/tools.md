# Tool and API reference

Contract reviewed against the main implementation and public service on 2026-10-29. Check capabilities on the service you use for current availability. X login is configured; Gmail and Pro payments are not enabled on the public service at this check.

Local stdio exposes 15 tools: the 14 hosted data/discovery tools plus **`get_usage`**, a client-side wrapper over REST. Limits are integers 1–200; local lists and social events default to 10, hosted lists to 200 and hosted social events to 20 per type. Smart Followers always returns at most 10 per pool.

| Local / hosted MCP tool | REST GET | Parameters | Credits |
| --- | --- | --- | ---: |
| `get_capabilities` | `/capabilities.json` (public), `/api/v1/capabilities` (key) | none | 0 |
| `get_usage` **local only** | `/api/v1/usage` | none | 0 |
| `get_leaderboard` | `/api/v1/leaderboards/influence` | sector, region, limit; kind=influence | returned rows |
| `get_leaderboard` | `/api/v1/leaderboards/weekly-growth` | sector, region, limit; kind=weekly_growth | returned rows |
| `get_kol_profile` | `/api/v1/kols/{handle}` | X handle | 1 |
| `get_kol_ranks` | `/api/v1/kols/{handle}/ranks` | handle | 1 |
| `get_smart_followers` | `/api/v1/kols/{handle}/smart-followers` | handle, sector | actual accounts across both pools, up to 20 |
| `get_kol_social` | `/api/v1/kols/{handle}/social` | handle, limit **per type** | actual events across four types, up to 4 × limit |
| `get_profile_history` | `/api/v1/kols/{handle}/profile-history` | handle | 1 per handle |
| `get_ability_model` | `/api/v1/kols/{handle}/abilities` | handle, sector | 1 |
| `get_weekly_kols` | `/api/v1/weekly/kols` | sector, region, mode, limit | returned rows |
| `get_binance_square_leaderboard` | `/api/v1/binance-square/leaderboard` | limit | returned rows |
| `get_binance_square_profile` | `/api/v1/binance-square/kols/{square_uid}` | immutable UID | 1 |
| `get_binance_square_abilities` | `/api/v1/binance-square/kols/{square_uid}/abilities` | immutable UID | 1 |
| `get_binance_square_weekly_trending` | `/api/v1/binance-square/weekly/trending` | metric, limit | returned rows |
| `get_youtube_leaderboard` | `/api/v1/youtube/leaderboard` | sector, limit | returned rows |

The existing Square alias `/api/v1/leaderboards/binance-square` shares billing/rate counters with the canonical route. Sector is `ai` or `web3`; X region is `global`, `en` or `cn`. X handles accept an optional leading `@` in the client. Square UIDs come from leaderboard rows; they are not usernames or X handles.

## Weekly definitions

| Feature | Exact meaning | Restrictions |
| --- | --- | --- |
| X `kind=weekly_growth` | Previous rank minus current rank over approximately seven days | AI/Web3, global/en/cn; inspect actual available count |
| X `mode=attention` | New attention from the monitored KOL network | Web3 only, cn/en only; not raw follower-count growth |
| X `mode=new_entries` | Current Top200 minus a comparable seven-day baseline | Includes re-entries; returns insufficient_history until a baseline exists |
| Square `metric=followers` | Absolute net total follower gain over seven days | Current influence Top1000; requires measured counts at both ends |
| Square `metric=smart_followers` | Absolute net gain in monitored source accounts following the KOL | Same candidate pool; source pool must be comparable |

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

X profiles include recorded current profile fields and known person/project and Chinese/international classifications. Six-rank aggregates include project ranks when available, but authoritative population counts are unavailable (`kol_count=null`). Smart Followers preserves the source ordering, at most 10 per global/cn pool per sector, with unknown classifications left null. International classification does not verify English language.

Social covers monitored following, followed, unfollowing and unfollowed events. The limit is per event type, not a time window. Unfollows cover approximately the last hour; follow records use the source's recent-observation filter. Missing arrays are unavailable, not evidence of no activity. Profile history is recorded snapshots in source order, not lifetime coverage or inferred effective change times.

Circle, a complete Following KOLs list, raw timelines/tweet search and cross-platform identity matching remain unavailable.

There are no YouTube profile/ability or real-time streaming endpoints in this contract. Data cadence is not an uptime or freshness guarantee; capabilities and metadata take precedence.
