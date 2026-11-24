import unittest

import httpx

from influence_client.client import InfluenceClient


class MetadataTest(unittest.IsolatedAsyncioTestCase):
    async def test_preserves_page_receipt_freshness_and_rate_headers(self):
        body = {'data': {'global': {'items': [{}] * 10}, 'cn': {'items': [{}] * 10}},
                'meta': {'billing': {'credits_charged': 1, 'unit': 'successful_nonempty_page'},
                         'freshness': {'snapshot_at': None, 'status': 'snapshot_time_unknown'}}}
        client = InfluenceClient(api_key='offline-test-key')
        await client.aclose()
        client._http = httpx.AsyncClient(base_url='https://example.test', transport=httpx.MockTransport(
            lambda _: httpx.Response(200, json=body, headers={
                'X-Credits-Charged': '1', 'X-Request-ID': 'audit-request',
                'X-RateLimit-Remaining': '119', 'X-RateLimit-Endpoint-Day-Remaining': '99'})))
        self.addAsyncCleanup(client.aclose)
        response = await client.x_smart_followers('alice')
        self.assertEqual(response['meta'], body['meta'])
        self.assertEqual(response['_client']['credits_charged'], 1)
        self.assertEqual(response['_client']['request_id'], 'audit-request')
        self.assertEqual(response['_client']['rate_limits'], {
            'x-ratelimit-remaining': '119', 'x-ratelimit-endpoint-day-remaining': '99'})

    async def test_application_user_agent_sent_for_public_and_authenticated_requests(self):
        requests = []

        def respond(request):
            requests.append(request)
            return httpx.Response(200, json={"ok": True})

        client = InfluenceClient(api_key="offline-test-key", base_url="https://example.test")
        self.addAsyncCleanup(client.aclose)
        client._http._transport = httpx.MockTransport(respond)
        await client.capabilities()
        await client.usage()
        self.assertEqual(len(requests), 2)
        for request in requests:
            self.assertEqual(request.headers["user-agent"], "XHunt-Influence-Client/0.1.0")
        self.assertNotIn("x-api-key", requests[0].headers)
        self.assertEqual(requests[1].headers["x-api-key"], "offline-test-key")
