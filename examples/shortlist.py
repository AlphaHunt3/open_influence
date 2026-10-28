"""Explicit two-platform shortlist. Up to 10 credits; reads XHUNT_API_KEY."""
import asyncio
import json

from influence_client import InfluenceClient


async def main():
    async with InfluenceClient() as client:
        # Deliberately explicit calls: no hidden fan-out or score merging.
        x = await client.x_leaderboard(sector="ai", region="global", limit=5)
        youtube = await client.youtube_leaderboard(sector="ai", limit=5)
        print(json.dumps({"x": x, "youtube": youtube}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
