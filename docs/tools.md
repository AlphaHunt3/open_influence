# Tool, CLI and Python reference

Checked 2026-11-25 against the public OpenAPI, capabilities and current implementation. Local stdio and hosted MCP each expose **20 tools**, including `get_usage`. All listed operations are read-only; account and payment actions belong on the website.

## Access limits and cost

Main influence rankings return up to100 accounts on Free; the separate Pro ranking endpoint returns up to500 with an active Pro account. KOL rankings cost0 credits, including Pro500.

For Smart Followers, social events, Circle, profile history, ability evidence, weekly KOL lists and hot lists, **a Free account can retrieve up to10 entries in each group; Pro can retrieve up to40**. A group means a follower pool, social event type, or evidence language/domain. These are access ceilings, not promises that the source contains enough records. Smart Followers requests the effective per-pool limit from the source; preserve `available_count`, `total_count` and `source_limited` when fewer eligible accounts exist.

CLI lists default to10. SDK and local MCP main rankings default to10; optional detail/weekly/hot limits default to the server-verified plan maximum. Explicit smaller requests are respected; requests above the plan ceiling are clamped by the server. Client validation allows1–100 (Pro rankings1–500). Weekly rank gain uses the per-group10/40 limit, even though accessed through `get_leaderboard`.

| MCP tool | CLI command | Python method | REST GET | Credits |
| --- | --- | --- | --- | --- |
| `get_capabilities` | `capabilities` | `capabilities()` | `/capabilities.json` | 0; local discovery needs no key; hosted MCP requires a key |
| `get_usage` | `usage` | `usage()` | `/api/v1/usage` | 0 |
| `get_leaderboard` | `x` | `x_leaderboard()` | `/api/v1/leaderboards/influence` | 0 |
| `get_leaderboard` with `kind=weekly_growth` | `x --kind weekly_growth` | `x_leaderboard(kind="weekly_growth")` | `/api/v1/leaderboards/weekly-growth` | 0 |
| `get_pro_leaderboard` | `pro` | `pro_leaderboard()` | `/api/v1/pro/leaderboards/{platform}` | 0; active Pro required |
| `get_kol_profile` | `profile HANDLE` | `x_profile(handle)` | `/api/v1/kols/{handle}` | 1 |
| `get_kol_ranks` | `ranks HANDLE` | `x_ranks(handle)` | `/api/v1/kols/{handle}/ranks` | 1 |
| `get_smart_followers` | `smart-followers HANDLE` | `x_smart_followers(handle)` | `/api/v1/kols/{handle}/smart-followers` | 1 per successful nonempty page across all three groups |
| `get_kol_social` | `social HANDLE` | `x_social(handle)` | `/api/v1/kols/{handle}/social` | 1 per successful nonempty page across all four types |
| `get_kol_circle` | `circle HANDLE` | `x_circle(handle)` | `/api/v1/kols/{handle}/circle` | 1 per successful nonempty page, including cached data |
| `get_profile_history` | `profile-history HANDLE` | `x_profile_history(handle)` | `/api/v1/kols/{handle}/profile-history` | 1 per successful nonempty page |
| `get_ability_model` | `abilities HANDLE` | `x_abilities(handle)` | `/api/v1/kols/{handle}/abilities` | 1 per model |
| `get_weekly_kols` | `weekly` | `x_weekly()` | `/api/v1/weekly/kols` | 0 |
| `get_binance_square_leaderboard` | `square` | `square_leaderboard()` | `/api/v1/binance-square/leaderboard` | 0 |
| `get_binance_square_profile` | `square-profile UID` | `square_profile(uid)` | `/api/v1/binance-square/kols/{square_uid}` | 1 |
| `get_binance_square_abilities` | `square-abilities UID` | `square_abilities(uid)` | `/api/v1/binance-square/kols/{square_uid}/abilities` | 1 |
| `get_binance_square_weekly_trending` | `square-weekly` | `square_weekly()` | `/api/v1/binance-square/weekly/trending` | 0 |
| `get_youtube_leaderboard` | `youtube` | `youtube_leaderboard()` | `/api/v1/youtube/leaderboard` | 0 |
| `get_hot_kols` | `hot-kols` | `hot(kind="hot-kols")` | `/api/v1/trending/hot-kols` | 0 |
| `get_hot_tweets` | `hot-tweets` | `hot(kind="hot-tweets")` | `/api/v1/trending/hot-tweets` | 1 per successful nonempty request |
| `get_rising_tweets` | `rising-tweets` | `hot(kind="rising-tweets")` | `/api/v1/trending/rising-tweets` | 1 per successful nonempty request |

Empty results and failed requests cost0; a missing billing header means unknown, not0. Tweet-feed pricing applies to Free and Pro regardless of returned count. Browsing the KOL website costs no credits. [Allowances, permanent credits and payments](billing.md).

## Parameters and examples

Sector is `ai` or `web3`. X influence region is `global`, `en` or `cn`; `en` is an international source pool, not a verified English-only filter. Hot lists and weekly attention offer separate `cn`/`en` pools. Handles accept an optional leading `@`; Square uses an immutable UID from a Square leaderboard, not an X handle.

```bash
uv run influence-client x --sector ai --region global --limit 10
uv run influence-client pro --platform youtube --sector web3 --limit 500
uv run influence-client smart-followers VitalikButerin --sector web3 --limit 2
uv run influence-client social VitalikButerin --limit 2
uv run influence-client circle VitalikButerin --days 30 --limit 2
uv run influence-client profile-history VitalikButerin --limit 2
uv run influence-client abilities VitalikButerin --sector web3 --limit 2
uv run influence-client weekly --sector ai --region cn --limit 10
uv run influence-client hot-kols --sector ai --region en --days 7 --limit 10
uv run influence-client hot-tweets --sector ai --region cn --limit 10
uv run influence-client rising-tweets --sector ai --region cn --limit 10
uv run influence-client square-weekly --metric smart_followers --region cn --limit 10
```

These are explicit individual calls, not a script to run all at once. Detail calls and tweet feeds may consume credits. The source may not have records for every example handle. `--limit` is supported by every list command, including profile history, followers, Circle and ability evidence. Hot KOLs support `--days 1` (today) or `--days 7` (this week); tweet feeds retain their own source window. Pro accepts `--platform x|binance-square|youtube`; regional Pro pools apply to X and Square; YouTube accepts only global.

## Weekly definitions

| Feature | Meaning | Coverage |
| --- | --- | --- |
| X `kind=weekly_growth` | Previous rank minus current rank over approximately7 days | AI/Web3 × global/en/cn; source shortages possible |
| X `mode=attention` | Distinct new active Smart Followers observed over 7 days, count descending (`new_smart_followers`) | AI/Web3 × cn/en; not raw total-follower growth |
| X `mode=new_entries` | Current Top200 minus a comparable seven-day baseline | Includes re-entries; missing baseline returns `insufficient_history` |
| Square `metric=followers` | Absolute net total-follower gain over7 days | Current influence Top1000; measured counts required |
| Square `metric=smart_followers` | Absolute net change in monitored source followers | Same candidate pool; comparable source pool required |

Weekly attention counts distinct newly observed active Smart Follower relationships. Publications refresh hourly and expire after six hours; an expired publication is regenerated on demand. Observation time is not the exact X follow timestamp. Web3 language groups refer to the observer pool; AI additionally requires targets in its regional AI candidate pool and applies the target language classification. Missing candidates do not establish that a person is unrelated to AI.

Square `region=global|en|cn` filters published account language before limiting; unknown language stays global-only. Inspect `weekly_regions` in capabilities. The SDK rejects rows from a server that fails to confirm a requested language pool, rather than silently calling them Chinese or English. `available_count` describes eligible rows, and `influence_rank` keeps the global influence rank. Missing counts are unknown, not zero.

## Ranking and abilities

- X influence is ranked by Smart Followers in the KOL network, with separate sectors and regions. Weekly rank gain, attention and hot engagement are distinct metrics.
- Square influence uses network following/quote contributions and breadth of support. Some source accounts may contribute to scoring while being excluded from the public ranking. Scores are not a fraud verdict.
- YouTube uses the published weekly multi-dimensional channel score; Web3 maps to the collector’s Crypto category. Preserve `week_id`, `method_ver`, `source_updated_at` and the collection window. The service reads ready reports, not live video search.
- X/Square abilities expose published scores >=85. X evidence groups contain original analysis posts where recovered; historical missing evidence remains explicit. Never replace it with unrelated recent tweets.

Scores are platform-specific. Combine shortlists, not scores; similar names do not prove the same identity.

## Responses and errors

Keep returned metadata intact. Lists generally use `{items, meta}`, while profiles/models use `{data, meta}`. `_client.credits_charged` records the actual response header; null means absent. The SDK does not infer success, freshness or zero cost from an empty body.

| Status | What to do |
| --- | --- |
| `available` | Inspect source timestamps and coverage |
| `insufficient_history` | No comparable baseline; do not fabricate rows |
| `insufficient_coverage` | Fewer qualifying accounts than the advertised maximum; do not pad results |
| `stale_data` | Inspect original source/cache time; it is not a current observation |
| `pending` | Circle SQL timed out; retry the same request after `meta.retry_after_seconds`, without automatic polling |
| 401 | Correct the private key or create a new one |
| 403 `pro_required` | Active Pro required; topping up credits does not grant it |
| 404 | Missing account/model or unavailable endpoint |
| 422 | Invalid or unsupported parameters |
| 429 `rate_limited` | Respect `Retry-After` |
| 429 `quota_exceeded` | Check usage; a short pause does not restore credits |
| 5xx | Service/source failure; not a successful empty example |

Errors and timeouts are never retried automatically. An interrupted data request may already have been charged.

## Coverage boundaries

Smart Followers uses the dedicated AI/Web3 follower endpoints with the effective per-pool limit (up to10 on Free or40 on Pro). A pool with fewer eligible accounts returns fewer rows; inspect returned totals and coverage rather than assuming the list is complete. Unknown classifications remain null. Six-rank population counts depend on fresh validated source cohorts; missing/stale counts remain null with a status.

Social is monitored activity, not all X history. Limits apply separately to following, followed, unfollowing and unfollowed. Free accounts see unfollow events older than72 hours; Pro has no plan time cutoff, subject to available confirmed records. The source confirmation delay is separate from this rule. Profile history is newest-first recorded snapshots, not lifetime history.

Circle measures observed direct replies/quotes/reposts, at least one action in each direction. Ordering uses total unique interaction posts, minimum directional count, then account ID. Missing references remain partial. Cache refresh starts after5 minutes; stale snapshots remain explicitly marked and cannot be served after1 hour without successful recomputation. Cached results retain normal billing. Only a confirmed SQL timeout with the durable cache available returns HTTP202 `pending`; other failures remain errors. Pending has no rows and costs0. Background login prewarming does not itself cost credits.

Pro authorization is checked server-side for the current account; high X rank, organization credits and top-ups do not grant Pro. Current publication metadata determines source count and date, not an old fixed channel total. No wallets or legacy migration are needed for this login flow.

A complete Following KOLs list, arbitrary tweet search/raw timelines, automatic cross-platform identity matching, standalone YouTube profile/ability APIs, soul index, ability leaderboards and soul leaderboards are not offered by this client.

## Billing, freshness and request diagnostics

`meta.billing` reports the actual charged credits and billing unit. Followers, Social, Circle and Profile History are billed once per successful nonempty page, including all records/groups, not per row. Empty results, pending calculations and failures cost zero.

`meta.freshness` distinguishes a published snapshot date from computation time. `snapshot_at=null` and `status=snapshot_time_unknown` explicitly mean no unified snapshot time is known; `served_at` is only the response time. Component dates preserve separate weekly/daily/baseline meanings. Ability model `model_generated_at` is the original published model generation time, even for older models; it does not establish when all input posts were collected. Never substitute an event date, database row update or today's date for a missing snapshot.

The SDK preserves response headers in `_client.rate_limits` and the correlation ID in `_client.request_id`; missing values remain absent/null, not invented. `x-ratelimit-*` describes the account's rolling global minute; `x-ratelimit-day-*`, `x-ratelimit-endpoint-*`, `x-ratelimit-endpoint-day-*` describe the other three buckets. Reset values are absolute Unix seconds. All keys and equivalent REST/MCP paths share counters; admitted requests include the current call, rejected calls do not increment them. Discovery/usage omit these headers because they do not consume data quota. For 429, respect `Retry-After`.

Authentication error codes: `missing_api_key`, `invalid_api_key`, `key_revoked`, `invalid_authentication_header`, `conflicting_api_keys`. Hosted OpenAPI error responses reference `components.schemas.Error`: `error.code` and `error.message` are required; source/validation errors additionally include `retryable` and `http_status`, while authentication/quota errors may omit them. Returned error responses cost zero credits. Data errors distinguish `kol_not_found` (X handle or Square UID absent from the source dataset; both Square profile and abilities return HTTP 404), `invalid_handle`/`invalid_parameters` (fix input), and source failures/timeouts (retry with backoff). Hosted MCP tool errors use `isError=true` plus `structuredContent.error`; HTTP200 alone does not establish success. API-key MCP does not provide OAuth login; see [client setup](clients.md).


### X score and tweet-body coverage

Weekly and hot MCP tools publish only `cn` and `en` pools; they do not accept `global`. REST weekly `mode=new_entries` separately supports `global`. X combined influence rankings expose the published Smart Follower voter count as `score` when available; cn/en sources publish positions without their historical score. Inspect `score_status` and `meta.score_metric`, preserve unknown values, and do not substitute ordinary followers or current Smart Follower totals. Rank-gain `score` measures positions gained. Hot tweets now include archived original `tweet.text` when recorded, with `text_status` distinguishing archived, missing, deleted and source-unavailable bodies. AI summaries are not original text.

## Regions: global / en / cn

`region` has two meanings. Read each capability's `regions`, `region_semantics` and `region_note`; top-level `regions_union` is only the union across endpoints, not a promise that every endpoint accepts every value. Capabilities without a region selector use `regions=[]` and `region_semantics=null`; no region filter is implied.

- **A — `author_language`**: account-language/source pools, not geography. For X, `en` maps to the upstream international/non-Chinese-classified pool and is **not a verified English-only filter**. `cn` uses the Chinese classification (the classifier examines up to 20 collected posts and marks Chinese when at least 20% contain Chinese). `global` maps to the upstream combined `all` ranking; independent pool construction means it is not a guaranteed exact union of regional ranked lists. Missing classification can enter the international pool.
- For **Square**, A filters the published `account.language`: `en` or `en-*`; `cn`, `zh` or `zh-*`. Unknown/other languages are included only in `global`. Therefore Square `global` covers all published languages, **not just en + cn**. This is a language filter, not geography or newly verified publishing history. Pro and weekly trending filter before limiting, using the same matching rules. YouTube offers only an unsplit `global` channel pool; it does not apply a channel-language filter.
- **B — `audience`**: en/cn select the international/Chinese KOL attention pools whose observed follows/interactions drive the ranking. They do **not guarantee the language of the returned account or post**. Source candidate restrictions still apply: AI weekly attention additionally requires targets in its regional AI candidate pool and applies their Chinese classification; hot-KOL sources also use regional candidate/account rules. Rising tweet sources additionally check normalized text for Chinese vs non-Chinese (non-Chinese is not English). For rising, `audience` labels the source scope, not the language of individual viewers: the score is observed view velocity and recall can include authors outside the ranked KOL pools. These are existing source rules, not a universal author-language filter.

| Tool / REST capability | Semantics | global | en | cn | Default |
|---|---|---|---|---|---|
| `get_leaderboard` (influence or rank gains) | A, X source pools | Yes | Yes | Yes | global |
| `get_pro_leaderboard`, x | A, X source pools | Yes | Yes | Yes | global |
| `get_pro_leaderboard`, binance-square | A, published account language | Yes | Yes | Yes | global |
| `get_pro_leaderboard`, youtube | A, unsplit channel pool | Yes | 422 | 422 | global |
| `get_weekly_kols`, attention | B, new Smart Follower observers; AI target restriction | 422 | Yes | Yes | cn |
| `get_hot_kols` | B, engagement with source candidate restrictions | 422 | Yes | Yes | cn |
| `get_hot_tweets` | B, KOL attention pool | 422 | Yes | Yes | cn |
| `get_rising_tweets` | B, plus source text-language check | 422 | Yes | Yes | cn |
| `get_binance_square_weekly_trending` | A, published account language | Yes | Yes | Yes | global |
| Square / YouTube public leaderboard (no region parameter) | A, unsplit publication | Implicit | — | — | global |
| REST `/weekly/kols?mode=new_entries` | A, X source pools | Yes | Yes | Yes | cn |

On hosted REST/MCP, `english` aliases `en` except Square weekly trending, whose enum remains `global/en/cn`. The local CLI/stdio client accepts canonical `en`, not the hosted `english` alias. Hosted `get_weekly_kols` keeps its existing cn/en-only schema even for `mode=new_entries`; REST new_entries accepts global. YouTube Pro rejects every non-global region. Unsupported regions return 422 `invalid_region` with canonical `error.supported_regions`; aliases are described in parameter schemas. Error responses cost zero credits. Successful region-bearing responses include `meta.region_semantics` and a source-specific `meta.region_note`.

## Tweet sectors: web3 / ai

| Tool | Sector meaning | Content filtering | Caller action |
|---|---|---|---|
| `get_hot_tweets` | KOL circle that surfaced the post | No sector-content relevance guarantee | Filter `tweet.ai.domain_tag` if relevance is required; missing domain_tag is unknown |
| `get_rising_tweets` | AI domain labels with post/author/link/media/conversation context where available | AI classification, not text-only relevance | Inspect the post and source domain classification; classifications can be wrong |

Hot tweets can be about topics outside the chosen sector: popularity in a Web3/AI circle is not proof of Web3/AI content. Rising Web3 selection admits `crypto`-labeled candidates, including relevant conversation context for replies; classification versions differ across source pools. Author, linked and media context can affect the classification, so a political/news post can qualify or be misclassified. AI has its own classified source pool. Neither a crypto account nor an AI label is a guarantee that each post is on topic; do not describe rising tweets as strictly content-verified.


### Hot tweet content classification

Filter hot-tweet content using `tweet.ai.domain_tag`. `sector=web3/ai` selects the KOL attention circle, not a content filter. Match the following **exact raw strings**; cn and en pools use the same values:

| API value (exact match) | English display name only |
| --- | --- |
| `crypto` | Crypto |
| `ai` | AI |
| `科技` | Technology |
| `金融` | Finance |
| `内容创作` | Content Creation |
| `抽奖` | Giveaway |
| `其他` | Other |

For Web3 content, use `domain_tag == "crypto"`; for AI content, use `domain_tag == "ai"`. Match other categories using the Chinese strings above. English display names are not API values: do not match `Crypto`, `AI`, `Technology`, `Finance`, `Content Creation`, `Giveaway` or `Other`. Do not translate or change the case of returned values. Missing/null classification is unknown, not `其他`.

```python
web3_items = [item for item in response["items"]
              if ((item.get("tweet") or {}).get("ai") or {}).get("domain_tag") == "crypto"]
```

Classification can be wrong; inspect original content when strict relevance matters. This is client-side filtering of the returned page: it does not change source ranking, refill filtered rows or reduce the nonempty request's credit price.

## Reading grouped response fields

- Smart Followers: choose **one** `sector=web3` or `sector=ai` per request. The three output pools are `data.global.items` (global KOL followers), `data.cn.items` (Chinese KOL followers), and `data.top.items` (Top100 KOL followers), within that sector. There are no `data.ai` or `data.web3` groups. Pool metadata (`available_count`, `total_count`, `returned_count`, `source_limited`, `status`) lives alongside `items`. Fewer than the requested limit can mean fewer eligible accounts in that pool. Pools may overlap.
- Social: read `data.following.events`, `data.followed.events`, `data.unfollowing.events` and `data.unfollowed.events`. Each type is an object with an `events` array and `status`, not an array itself and not an `items` group. Missing/wrong JSON paths must not be reported as empty results. All four actual event arrays empty means zero credits; any events across these types means one credit for the page. Compare `meta.billing.returned_count` and `meta.billing.credits_charged` with the response header `X-Credits-Charged`. `unfollow_evaluated_at` is filter evaluation time, not an upstream ingestion timestamp; use `meta.freshness` for published snapshot information.
- Rising tweets: each `items[]` contains only `rank`, `id`, `burst_speed` and nested `tweet`. The API does not expose predictive model metrics. Read original content from `tweet.text` and author data from `tweet.profile`; do not interpret absent model fields as zero.
