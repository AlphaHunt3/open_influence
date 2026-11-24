#!/usr/bin/env bash
# Explicit example: KOL leaderboard costs 0 credits; authentication and rate limits apply. Configure XHUNT_API_KEY privately first.
set -euo pipefail
: "${XHUNT_API_KEY:?Set XHUNT_API_KEY privately before running}"
curl --fail-with-body --silent --show-error \
  -H "X-API-Key: ${XHUNT_API_KEY}" \
  'https://mcp.xhunt.ai/api/v1/youtube/leaderboard?sector=ai&limit=5'
