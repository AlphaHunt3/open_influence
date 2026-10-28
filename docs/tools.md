# Tool and API reference

Contract reviewed against `/root/xhunt-auth-billing` on 2026-10-28, branch `feat/influence-auth-billing`, base commit `089c936f97ee839dcf0283af2567c1d39a1e8dc1` plus in-progress changes. The worktree, not the older public deployment, is the implementation reference. Call capabilities on the service you use to discover current availability.

Local stdio exposes the same 10 hosted data/discovery tools plus **`get_usage`**, a client-side wrapper over REST. Limits are integers 1–200; local lists default to 10, hosted lists to 200.

| Local / hosted MCP tool | REST GET | Parameters | Credits |
| --- | --- | --- | ---: |
| `get_capabilities` | `/capabilities.json` (public), `/api/v1/capabilities` (key) | none | 0 |
| `get_usage` **local only** | `/api/v1/usage` | none | 0 |
| `get_leaderboard` | `/api/v1/leaderboards/influence` | sector, region, limit; kind=influence | returned rows |
| `get_leaderboard` | `/api/v1/leaderboards/weekly-growth` | sector, region, limit; kind=weekly_growth | returned rows |
| `get_kol_profile` | `/api/v1/kols/{handle}` | X handle | 1 |
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

The public Influence API **does not yet provide** Smart Followers Top10 lists, Following KOLs, Circle, raw timelines/tweet search, social follow/unfollow events, profile-change history, a six-rank-per-handle aggregate, project-specific rank or cross-platform identity matching. Some underlying sources may have these, but this client advertises only the implemented public contract. Account type is available in Square where published; it is not guaranteed by X profile responses.

There are no YouTube profile/ability or real-time streaming endpoints in this contract. Data cadence is not an uptime or freshness guarantee; capabilities and metadata take precedence.
