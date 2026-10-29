"""Verify a wheel installation, not an editable checkout. No retries or fan-out."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
import subprocess
import sys

import influence_client
from influence_client import InfluenceClient, InfluenceError
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def payload(result):
    assert not result.isError, 'MCP returned a tool error'
    if result.structuredContent is not None:
        return result.structuredContent
    return json.loads(''.join(item.text for item in result.content if item.type == 'text'))


async def verify(offline):
    package = Path(influence_client.__file__).resolve()
    assert package.is_relative_to(Path(sys.prefix).resolve()), 'Install the wheel into a clean venv; editable/source imports are not accepted'
    executable = str(Path(sys.executable).parent / 'influence-client')
    env = {key: value for key, value in os.environ.items() if key != 'PYTHONPATH'}
    if offline:
        env.update(XHUNT_API_KEY='', XHUNT_BASE_URL='http://127.0.0.1:1')
        env.pop('XHUNT_FREE_TEST_KEY', None)
    else:
        assert env.get('XHUNT_INSTALL_TEST') == '1', 'Explicit isolated-install-test opt in required'
        assert env.get('XHUNT_BASE_URL') == 'http://127.0.0.1:18893', 'Only isolated loopback API18893 is allowed'
        assert env.get('XHUNT_API_KEY', '').startswith('xh_'), 'Use an isolated personal Pro key'
        assert env.get('XHUNT_FREE_TEST_KEY', '').startswith('xh_'), 'Provide a separate isolated free personal key'
    help_result = subprocess.run([executable, '--help'], env=env, capture_output=True, text=True, timeout=30)
    assert help_result.returncode == 0 and 'pro' in help_result.stdout and 'circle' in help_result.stdout
    spent = 0
    async with InfluenceClient(api_key=env['XHUNT_API_KEY'], base_url=env['XHUNT_BASE_URL']) as client:
        if offline:
            try:
                await client.usage()
            except InfluenceError as error:
                assert error.code == 'missing_api_key'
            else:
                raise AssertionError('Missing key should fail before any HTTP request')
        else:
            before = await client.usage()
            assert before['plan'] == 'pro' and before['monthly_cap'] == 30000
            result = await client.youtube_leaderboard(sector='ai', limit=1)
            assert len(result['items']) == result['_client']['credits_charged'] == 1
            spent += 1
            cli = await asyncio.to_thread(subprocess.run, [executable, 'pro', '--platform', 'youtube', '--sector', 'web3', '--limit', '1'],
                                          env=env, capture_output=True, text=True, timeout=45)
            assert cli.returncode == 0, 'Installed CLI Pro request failed'
            result = json.loads(cli.stdout)
            assert len(result['items']) == result['_client']['credits_charged'] == 1
            spent += 1
            async with InfluenceClient(api_key=env['XHUNT_FREE_TEST_KEY'], base_url=env['XHUNT_BASE_URL']) as free:
                free_before = await free.usage()
                try:
                    await free.pro_leaderboard(platform='youtube', limit=1)
                except InfluenceError as error:
                    assert error.status == 403 and error.code == 'pro_required'
                else:
                    raise AssertionError('Free key must not retrieve Pro rows')
                assert (await free.usage())['monthly_used'] == free_before['monthly_used']
        params = StdioServerParameters(command=executable, args=['serve'], env=env)
        async with stdio_client(params) as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()
                tools = {tool.name: tool for tool in (await session.list_tools()).tools}
                assert len(tools) == 17
                assert 'get_kol_circle' in tools and 'get_pro_leaderboard' in tools
                assert 'get_ability_leaderboard' not in tools and 'get_soul_leaderboard' not in tools
                schema = tools['get_pro_leaderboard'].inputSchema['properties']['limit']
                assert schema['maximum'] == 500 and schema['default'] == 10
                # These fail schema validation before a data query; also safe in offline CI.
                assert (await session.call_tool('get_kol_circle', {'handle': 'cz_binance', 'days': 31})).isError
                assert (await session.call_tool('get_pro_leaderboard', {'limit': 501})).isError
                if not offline:
                    payload(await session.call_tool('get_capabilities'))
                    usage = payload(await session.call_tool('get_usage'))
                    assert usage['monthly_used'] == before['monthly_used'] + spent
                    for tool, arguments in [
                        ('get_leaderboard', {'sector': 'ai', 'limit': 1}),
                        ('get_binance_square_leaderboard', {'limit': 1}),
                        ('get_youtube_leaderboard', {'sector': 'ai', 'limit': 1}),
                    ]:
                        result = payload(await session.call_tool(tool, arguments))
                        assert len(result['items']) == result['_client']['credits_charged'] == 1
                        spent += 1
                    result = payload(await session.call_tool('get_pro_leaderboard', {'platform': 'youtube', 'sector': 'web3', 'limit': 500}))
                    assert len(result['items']) == result['_client']['credits_charged'] == 429
                    assert result['status'] == 'insufficient_coverage'
                    spent += 429
        if not offline:
            after = await client.usage()
            assert after['monthly_used'] - before['monthly_used'] == spent == 434
    print(json.dumps({'installed_wheel': True, 'mode': 'offline' if offline else 'isolated-live',
                      'stdio_tools': len(tools), 'credits_charged': spent,
                      'verified': ['CLI entrypoint', 'installed Python SDK', 'actual stdio MCP initialize/list/call', 'Pro/Circle schema limits']
                          + ([] if offline else ['three platforms', 'free Pro denied', 'Web3 coverage429', 'shared actual ledger'])}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline', action='store_true', help='No data requests: CLI help, no-key SDK check and stdio schemas only.')
    args = parser.parse_args()
    asyncio.run(verify(args.offline))
