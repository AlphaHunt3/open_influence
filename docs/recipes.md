# Research recipes

These are prompts and workflows, not cached recommendations or invented sample output. The agent should show the live source timestamps and actual credit headers.

## A creator shortlist for a launch

```text
Find 10 Web3 KOLs in the Chinese X pool. From those results, select
three whose public profile seems relevant to our launch and fetch only
those three profiles and three ability models. Keep only published
abilities >=85. Show the source time, profile link, evidence and limits.
Do not infer a sponsorship price or claim these creators endorsed us.
```

Calls: one `get_leaderboard(limit=10)` + three profiles + three models. Maximum6 credits if all records are returned. Read capabilities first for0 credits. Avoid fetching all100 and then discarding90.

## Cross-platform AI watchlist

```text
Compare the top 5 AI creators on X global and YouTube. Return two
separate lists, with platform-specific rank, available metrics and source
time. Explain how each ranking works. Do not merge their scores or
assume similar names identify the same person. Maximum10 data credits.
```

Calls: `get_leaderboard(sector=ai,region=global,limit=5)` and `get_youtube_leaderboard(sector=ai,limit=5)`. The client does not hide this two-call cost behind a single tool.

## Rank momentum versus network attention

```text
Retrieve 5 Chinese Web3 X rank gainers and 5 weekly attention leaders.
Explain the difference between positions gained and KOL-network attention.
Include limitations and timestamps. Do not call either follower growth.
```

Calls: `get_leaderboard(kind=weekly_growth,sector=web3,region=cn,limit=5)` and `get_weekly_kols(mode=attention,sector=web3,region=cn,limit=5)`. Zero credits.

## Square growth watch

```text
First inspect current coverage. If Square weekly follower growth has a
comparable baseline, retrieve the top10. Explain that the candidate pool
is the current influence Top1000 and the measure is absolute net total
follower gain. If history is insufficient, show its expected baseline
date and stop; do not fabricate a trending list or poll repeatedly.
```

Use `get_binance_square_weekly_trending(limit=10,metric=followers)`. Zero credits for the ranking, including nonempty results. `smart_followers` is a different, monitored-network metric, not all followers.

## Run from a terminal

```bash
uv run influence-client x --sector web3 --region cn --limit 5
uv run influence-client x --kind weekly_growth --sector web3 --region cn --limit 5
uv run influence-client weekly --mode attention --region cn --limit 5
uv run influence-client youtube --sector ai --limit 5
uv run influence-client square-weekly --metric smart_followers --limit 5
```
