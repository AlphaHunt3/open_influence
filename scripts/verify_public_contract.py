"""Check SDK routes against public metadata; no key, data queries or credits."""
import asyncio
import json
import re

import httpx

from influence_client import InfluenceClient


async def main():
    origin = 'https://mcp.xhunt.ai'
    async with httpx.AsyncClient(timeout=20, follow_redirects=False) as public:
        schema_response = await public.get(origin + '/openapi.json')
        schema_response.raise_for_status()
        capability_response = await public.get(origin + '/capabilities.json')
        capability_response.raise_for_status()
    schema = schema_response.json()
    capabilities = capability_response.json()
    observed = []

    def record(request):
        observed.append(request)
        return httpx.Response(200, json={'items': [], 'meta': {'region': 'cn'}})

    async with InfluenceClient(api_key='offline-contract-placeholder') as client:
        await client._http.aclose()
        client._http = httpx.AsyncClient(base_url='https://example.test', transport=httpx.MockTransport(record))
        await client.capabilities()
        await client.usage()
        for kind in ('influence', 'weekly_growth'):
            await client.x_leaderboard(kind=kind)
        await client.x_profile('alice')
        await client.x_ranks('alice')
        await client.x_smart_followers('alice', limit=40)
        await client.x_social('alice', limit=40)
        await client.x_circle('alice', days=30, limit=40)
        await client.x_profile_history('alice', limit=40)
        await client.x_abilities('alice', sector='ai', limit=40)
        for mode in ('attention', 'new_entries'):
            await client.x_weekly(sector='ai', mode=mode, limit=40)
        await client.square_leaderboard()
        await client.square_profile('123')
        await client.square_abilities('123')
        await client.square_weekly(region='cn', limit=40)
        await client.youtube_leaderboard()
        for platform in ('x', 'binance-square', 'youtube'):
            await client.pro_leaderboard(platform=platform, limit=500)
        for kind in ('hot-kols', 'hot-tweets', 'rising-tweets'):
            await client.hot(kind=kind, sector='ai', limit=40)
        await client.hot(days=7, sector='ai')
    covered = set()
    for request in observed:
        matches = [(path, data['get']) for path, data in schema['paths'].items()
                   if 'get' in data and re.fullmatch(re.sub(r'\{[^}]+\}', r'[^/]+', path), request.url.path)]
        assert len(matches) == 1, f'Undocumented or ambiguous SDK path: {request.url.path}'
        path, operation = matches[0]
        covered.add(path)
        parameters = {item['name']: item for item in operation.get('parameters', []) if item['in'] == 'query'}
        for name, value in request.url.params.items():
            assert name in parameters, f'Unknown query parameter: {path} {name}'
            spec = parameters[name]['schema']
            spec = next((item for item in spec.get('anyOf', [spec]) if item.get('type') != 'null'), spec)
            if 'enum' in spec:
                assert value in [str(item) for item in spec['enum']], f'Unsupported enum: {path} {name}={value}'
            if spec.get('type') == 'integer':
                assert spec.get('minimum', 0) <= int(value) <= spec.get('maximum', float('inf')), f'Invalid bound: {path} {name}'
    # Authentication-only capability and Square alias routes are intentionally canonicalized.
    excluded = {'/api/v1/capabilities', '/api/v1/leaderboards/binance-square'}
    expected = {path for path, data in schema['paths'].items() if path.startswith('/api/v1/') and 'get' in data} - excluded
    assert expected <= covered, f'Public data routes missing from SDK: {sorted(expected - covered)}'
    assert capabilities['pro']['max_limit'] == 500
    assert capabilities['list_limits']['free']['detail_and_hot'] == 10
    assert capabilities['list_limits']['pro'] == 40
    assert capabilities['billing']['kol_leaderboards_and_trending'] == 0
    assert capabilities['billing']['tweet_feeds']['credits'] == 1
    page_billing = capabilities['billing']['account_list_pages']
    assert page_billing['credits'] == 1
    assert page_billing['unit'] == 'successful_nonempty_page'
    assert page_billing['all_groups_included'] is True
    assert page_billing['empty_pending_and_errors'] == 0
    print(json.dumps({'metadata_origin': origin, 'sdk_contract_cases': len(observed), 'documented_paths': len(covered),
                      'coverage': 'all canonical /api/v1 GET data routes', 'live_data_requests': 0,
                      'note': 'Route/schema and metadata validation; not authenticated data or payment acceptance.'}))


if __name__ == '__main__':
    asyncio.run(main())
