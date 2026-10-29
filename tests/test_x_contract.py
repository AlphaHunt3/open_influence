import unittest

import httpx

from influence_client.client import InfluenceClient, InfluenceError
from influence_client.server import server


class XContractTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.requests = []

        def respond(request):
            self.requests.append(request)
            return httpx.Response(200, json={
                "data": {"kol_count": None, "account_type": None},
                "meta": {"coverage": "monitored only"},
            }, headers={"X-Credits-Charged": "8"})

        self.client = InfluenceClient(api_key="local-test-key")
        await self.client._http.aclose()
        self.client._http = httpx.AsyncClient(
            base_url="https://example.test", transport=httpx.MockTransport(respond))
        self.addAsyncCleanup(self.client.aclose)

    async def test_handle_normalization_preserves_unknowns_coverage_and_charge(self):
        for call in (self.client.x_ranks, self.client.x_smart_followers,
                     self.client.x_social, self.client.x_circle, self.client.x_profile_history):
            result = await call("@Alice")
            self.assertIn("/kols/Alice/", self.requests[-1].url.path)
            self.assertIsNone(result["data"]["kol_count"])
            self.assertIsNone(result["data"]["account_type"])
            self.assertEqual(result["meta"]["coverage"], "monitored only")
            self.assertEqual(result["_client"]["credits_charged"], 8)
            self.assertEqual(self.requests[-1].headers["X-API-Key"], "local-test-key")

    async def test_invalid_inputs_never_send_a_billable_request(self):
        for limit in (False, 0, 201, 1.5):
            with self.assertRaises(InfluenceError):
                await self.client.x_social("alice", limit=limit)
        for call in (self.client.x_ranks, self.client.x_smart_followers,
                     self.client.x_social, self.client.x_circle, self.client.x_profile_history):
            with self.assertRaises(InfluenceError):
                await call("alice/../../usage")
        with self.assertRaises(InfluenceError):
            await self.client.x_smart_followers("alice", sector="unknown")
        for days in (False, 0, 31, 1.5):
            with self.assertRaises(InfluenceError):
                await self.client.x_circle("alice", days=days)
        self.assertEqual(self.requests, [])

    async def test_mcp_discovery_exposes_new_contract_and_bounded_social_limit(self):
        tools = {tool.name: tool for tool in await server.list_tools()}
        for name in ("get_kol_ranks", "get_smart_followers", "get_kol_social", "get_kol_circle", "get_profile_history"):
            self.assertIn(name, tools)
        window = tools["get_kol_circle"].inputSchema["properties"]["days"]
        self.assertEqual((window["minimum"], window["maximum"], window["default"]), (1, 30, 7))
        limit = tools["get_kol_social"].inputSchema["properties"]["limit"]
        self.assertEqual((limit["minimum"], limit["maximum"], limit["default"]), (1, 200, 10))

    async def test_square_old_server_cannot_masquerade_as_language_ranking(self):
        with self.assertRaises(InfluenceError) as error:
            await self.client.square_weekly(region="cn")
        self.assertEqual(error.exception.code, "unsupported_region")
        self.assertEqual(self.requests[-1].url.params["region"], "cn")
        # The original global contract remains compatible with older servers.
        await self.client.square_weekly()

    async def test_old_server_history_state_is_preserved_but_never_unverified_rows(self):
        payload = {"status": "insufficient_history", "items": [], "meta": {}}
        await self.client._http.aclose()
        self.client._http = httpx.AsyncClient(
            base_url="https://example.test",
            transport=httpx.MockTransport(lambda request: httpx.Response(200, json=payload)))
        result = await self.client.square_weekly(region="cn")
        self.assertEqual(result["status"], "insufficient_history")
        payload["items"] = [{"square_uid": "unverified"}]
        with self.assertRaises(InfluenceError):
            await self.client.square_weekly(region="cn")


if __name__ == "__main__":
    unittest.main()
