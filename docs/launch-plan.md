# GitHub launch plan: earn stars by making agents useful

Prepared2026-10-28. This is a release/measurement plan, not a promise of star counts or a claim that distribution steps have already happened.

## Positioning

Repository name: `influence-client` (requested). Public headline: **Influence MCP — give your AI agent a map of who matters in AI and Web3.**

Do not lead with “API SDK” or a long feature inventory. Lead with a task people want to repeat: a creator shortlist across X, Binance Square and YouTube, with source timestamps and clearly defined momentum. The most defensible distinction is influence/creator intelligence across three platforms, including Square, rather than generic tweet search. No “first,” “largest,” unlimited/free, fraud-proof or trading-return claims.

Keep one repository rather than splitting three small connectors and dividing stars. Make individual platform recipes discoverable inside it. Brand `Influence MCP` in the title/hero, retain `influence-client` as the package/repository name. Repository description proposal:

> AI agent influence intelligence across X, Binance Square & YouTube. MCP server + Python SDK + CLI. Discover AI/Web3 creators, expertise and weekly trends.

Homepage: `https://mcp.xhunt.ai`. Suggested topics: `mcp`, `mcp-server`, `model-context-protocol`, `ai-agents`, `claude`, `cursor`, `twitter`, `youtube`, `binance-square`, `web3`, `influencer-analytics`, `python`.

## What the two references demonstrate

Public GitHub API snapshot2026-10-28:

| Repository | Stars | Forks | Created |
| --- | ---: | ---: | --- |
| [6551Team/opennews-mcp](https://github.com/6551Team/opennews-mcp) | 2,423 | 194 | 2026-02-26 |
| [6551Team/opentwitter-mcp](https://github.com/6551Team/opentwitter-mcp) | 1,437 | 102 | 2026-02-26 |

Both visibly prioritize a token link, Claude Code command, Skill install, natural-language examples, tool table and multiple client configurations. They have English/Chinese/Japanese/Korean entry points. These are useful adoption patterns; their star totals do **not** establish what drove growth, referral traffic, the role of an existing community or causality. We inspected README, package metadata, license and repository metadata, not their private analytics. Our code/assets are independently authored.

What to copy in principle: shortest working install, outcome-first prompts, a small auditable client and direct agent Skills. What to improve: hosted install with no local checkout, clear per-result credit pricing, explicit10-row examples, honest feature/status coverage, no fake compatibility/release badges.

## Release gates, in order

1. Deploy/configure the auth-billing version and verify real X/Gmail sign-in, personal key creation and a5-result first call. The current account worktree is not deployment proof. Missing key signup is a launch blocker even when data endpoints work. Payment is optional for the first public preview; hide disabled purchase claims in announcements.
2. Publish this repository under the intended organization, set homepage/description/topics, enable issues/discussions if maintainers will answer, configure a private security reporting route. Ensure all relative docs/assets render publicly.
3. Publish a versioned GitHub release after package verification. Publish PyPI only after deciding package ownership and trusted publishing; do not claim `pip install influence-client` or `uvx influence-client` works before it exists. The current remote-MCP install avoids this dependency.
4. Record a real45–60second demo: connect → request10AI creators onX andYouTube → show source time, separate scoring and actual credits. Publish a short captioned GIF/MP4 or repository asset. Current SVG is a hero, not a recorded product demo.
5. Add social-preview artwork derived from `assets/hero.svg` through repository settings; GitHub preview requires a raster export. Use a recognizable dark green/lime look and a readable three-platform subtitle. No fake star badge or customer logos.
6. Validate the top two client configuration paths in real client apps and label their exact versions. The current protocol smoke checks are not a substitute for every app UI. Keep the main install command above the fold.

## First two weeks

| Window | Action | Useful output |
| --- | --- | --- |
| Before day1 | Fix signup/key/first-query friction with3–5 trusted users; ask permission before sharing their output | Working setup and one observed use case per user |
| Days1–2 | One English and one Chinese launch from owned channels, each showing a real workflow and the GitHub link | One demo, three example prompts, concrete call-cost example |
| Days2–4 | Submit to official MCP Registry if eligible, relevant MCP catalogs, and appropriate awesome lists following contribution rules | Searchable listing with exact tools and auth requirement |
| Days3–7 | Publish a useful “AI creator discovery acrossX/YouTube” recipe and a “Square influence vs follower count” explainer | Shareable research using current public API results, timestamps and method limits |
| Days5–10 | Collect actual client setup failures; fix onboarding and respond quickly to issues | Lower time-to-first-success, tagged patch release |
| Days8–14 | Share a second use-case-led update, e.g. a creator shortlist template; add a requested integration or translation | Real improvement, not “please star” repetition |

Potential communities: existing XHunt users, AI-agent developers, MCP/Claude/Cursor communities, Web3 research and creator-operations teams. Follow each channel’s rules; no automated unsolicited DMs, paid stars, star-for-credit incentives, fake accounts, duplicate spam or unsupported endorsements. Distribution and directory submissions are planned, not performed by this client.

If Square weekly history is still insufficient, demo influence and expertise instead. Do not make “weekly trending” the launch hero until real seven-day results exist.

## Measure the funnel, not only star count

Track weekly:

- GitHub unique visitors, views, clones and stars from repository Insights/API, respecting available retention limits.
- README→website clicks and website→account/key creation→first successful query via website-side consent/privacy practices. UTM links for owned campaigns can distinguish launch posts. No client telemetry is included.
- Setup completion, time-to-first-success and support failures by client, from volunteer feedback. Do not infer setup success from a clone.
- Successful data calls and7-day returning accounts from aggregated server metrics; no keys or query content in public reports.
- Issues answered, useful recipes contributed and actual use cases.

Stars/unique visitors is only a rough aggregate ratio: different windows, repeat visitors and delayed stars prevent precise attribution. Compare cohorts/periods carefully; do not call an increase causal without an experiment. Changing README, launch channel and free allowance simultaneously destroys attribution.

First experiment: compare outcome-focused launch copy against generic “MCP SDK” copy in two owned posts while keeping README/install path fixed. Second: offer a no-key capability demo and a5-result first data call, then observe signup/drop-off. Improve activation before expanding languages or directories. Translate Japanese/Korean after an actual reviewer is available; publishing unreliable translations is worse than useful EN/ZH.

## Retention and contribution loop

Use issues to request specific research recipes and client fixes. Link to a minimal successful example in every troubleshooting answer. Tag releases with an explanation of the user-visible improvement. Update tool docs when source capabilities change. Give contributors visible credit through normal Git history/releases and thank useful feedback without trading stars for access.

The strongest star loop is: a developer asks a useful question → sees a defensible result quickly → saves the repo → shares the reusable prompt or integration. A larger feature list alone does not create that loop.
