"""Cross-surface regressions against the published API contract; no network."""
import unittest
from unittest.mock import patch

import httpx

from influence_client import InfluenceClient, InfluenceError
from influence_client.cli import parser, run
from influence_client.server import server


class FeatureCoverageTest(unittest.IsolatedAsyncioTestCase):
    async def test_weekly_and_hot_schemas_exclude_unpublished_global_pool(self):
        tools = {tool.name: tool for tool in await server.list_tools()}
        for name in ("get_weekly_kols", "get_hot_kols", "get_hot_tweets", "get_rising_tweets"):
            self.assertEqual(set(tools[name].inputSchema["properties"]["region"]["enum"]), {"cn", "en"})
            self.assertIn("audience", tools[name].description)
            self.assertIn("audience", tools[name].inputSchema["properties"]["region"]["description"])

    async def asyncSetUp(self):
        self.requests = []
        self.status = 200
        self.payload = {"items": [], "meta": {"source_updated_at": "fixture-time"}}
        self.headers = {"X-Credits-Charged": "0"}

        def respond(request):
            self.requests.append(request)
            return httpx.Response(self.status, json=self.payload, headers=self.headers)

        self.client = InfluenceClient(api_key="test-private-key")
        await self.client._http.aclose()
        self.client._http = httpx.AsyncClient(base_url="https://example.test", transport=httpx.MockTransport(respond))
        self.addAsyncCleanup(self.client.aclose)

    async def test_ai_attention_and_rising_tweets_are_available_in_both_pools(self):
        for region in ("cn", "en"):
            await self.client.x_weekly(sector="ai", region=region, limit=40)
            self.assertEqual(self.requests[-1].url.path, "/api/v1/weekly/kols")
            self.assertEqual(dict(self.requests[-1].url.params), {"sector": "ai", "region": region, "mode": "attention", "limit": "40"})
            await self.client.hot(kind="rising-tweets", sector="ai", region=region, limit=40)
            self.assertEqual(self.requests[-1].url.path, "/api/v1/trending/rising-tweets")
            self.assertEqual(self.requests[-1].url.params["sector"], "ai")
        before = len(self.requests)
        with self.assertRaises(InfluenceError):
            await self.client.x_weekly(sector="ai", region="global")
        self.assertEqual(len(self.requests), before)

    async def test_new_cli_routes_forward_filters_and_limits(self):
        cases = [
            (["hot-kols", "--days", "7", "--sector", "ai", "--region", "en", "--limit", "40"], "hot", {"kind": "hot-kols", "days": 7, "sector": "ai", "region": "en", "limit": 40}),
            (["hot-tweets", "--sector", "ai", "--limit", "2"], "hot", {"kind": "hot-tweets", "sector": "ai", "region": "cn", "limit": 2}),
            (["rising-tweets", "--sector", "ai"], "hot", {"kind": "rising-tweets", "sector": "ai", "region": "cn", "limit": 10}),
            (["smart-followers", "alice", "--limit", "40"], "x_smart_followers", {"handle": "alice", "sector": "web3", "limit": 40}),
            (["circle", "alice", "--days", "30", "--limit", "40"], "x_circle", {"handle": "alice", "days": 30, "limit": 40}),
            (["profile-history", "alice", "--limit", "40"], "x_profile_history", {"handle": "alice", "limit": 40}),
            (["abilities", "alice", "--sector", "ai", "--limit", "40"], "x_abilities", {"handle": "alice", "sector": "ai", "limit": 40}),
        ]
        from unittest.mock import AsyncMock
        for argv, method, expected in cases:
            with self.subTest(argv=argv):
                client = AsyncMock()
                client.__aenter__.return_value = client
                with patch("influence_client.cli.InfluenceClient", return_value=client):
                    await run(parser().parse_args(argv))
                getattr(client, method).assert_awaited_once_with(**expected)

    async def test_cli_covers_every_sdk_data_operation(self):
        # Map public operations, not just command count: every API family needs an entry point.
        commands = {
            "capabilities": [], "usage": [], "x": [], "pro": [], "profile": ["alice"],
            "ranks": ["alice"], "smart-followers": ["alice"], "circle": ["alice"],
            "social": ["alice"], "profile-history": ["alice"], "abilities": ["alice"],
            "weekly": [], "square": [], "square-profile": ["123"], "square-abilities": ["123"],
            "square-weekly": [], "youtube": [], "hot-kols": [], "hot-tweets": [], "rising-tweets": [],
        }
        from unittest.mock import AsyncMock
        for name, args in commands.items():
            with self.subTest(command=name):
                client = AsyncMock()
                client.__aenter__.return_value = client
                with patch("influence_client.cli.InfluenceClient", return_value=client):
                    await run(parser().parse_args([name, *args]))
                self.assertEqual(sum(v.await_count for k, v in client._mock_children.items() if not k.startswith("__")), 1)
        tools = {tool.name for tool in await server.list_tools()}
        self.assertEqual(len(tools), len(commands))

    async def test_circle_pending_is_preserved_without_retry_or_charge(self):
        self.status = 202
        self.payload = {"status": "pending", "items": [], "meta": {"reason": "circle_sql_timeout", "retry_after_seconds": 30}}
        result = await self.client.x_circle("alice", days=30)
        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["meta"]["retry_after_seconds"], 30)
        self.assertEqual(result["_client"]["credits_charged"], 0)
        self.assertEqual(len(self.requests), 1)

    async def test_usage_preserves_permanent_balance_and_allowance_fields(self):
        self.payload = {"plan": "free", "monthly_remaining": 500, "daily_remaining": 0,
                        "purchased_remaining": 4000, "available_today": 4000, "total_remaining": 4500}
        result = await self.client.usage()
        self.assertEqual({k: result[k] for k in self.payload}, self.payload)
        self.assertEqual(result["_client"]["credits_charged"], 0)

    async def test_errors_do_not_echo_secrets_and_never_retry(self):
        self.status = 429
        self.payload = {"error": {"code": "quota_exceeded", "message": "test-private-key https://private.test"}}
        self.headers = {"Retry-After": "60"}
        with self.assertRaises(InfluenceError) as caught:
            await self.client.hot("hot-tweets", limit=1)
        self.assertEqual(caught.exception.code, "quota_exceeded")
        self.assertEqual(caught.exception.retry_after, "60")
        self.assertNotIn("test-private-key", str(caught.exception))
        self.assertNotIn("private.test", str(caught.exception))
        self.assertEqual(len(self.requests), 1)

    async def test_missing_charge_remains_unknown(self):
        self.headers = {}
        result = await self.client.youtube_leaderboard(limit=1)
        self.assertIsNone(result["_client"]["credits_charged"])
