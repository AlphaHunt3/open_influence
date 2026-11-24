"""Offline documentation links and MCP/CLI coverage. No API calls."""
import argparse
import asyncio
from pathlib import Path
import re
from urllib.parse import unquote

from influence_client.cli import parser
from influence_client.server import server


async def main():
    root = Path(__file__).resolve().parents[1]
    errors = []
    files = [*root.glob('*.md'), *root.glob('docs/**/*.md'), *root.glob('skills/**/*.md')]
    for path in files:
        text = path.read_text()
        targets = re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text)
        targets += re.findall(r'<img[^>]+src="([^"]+)"', text)
        for target in targets:
            if target.startswith(('#', 'http:', 'https:', 'mailto:')):
                continue
            local = unquote(target.split('#')[0])
            if local and not (path.parent / local).exists():
                errors.append(f'{path.relative_to(root)}: missing {local}')
    reference = (root / 'docs/tools.md').read_text()
    tools = await server.list_tools()
    for tool in tools:
        if f'`{tool.name}`' not in reference:
            errors.append(f'Missing MCP tool documentation: {tool.name}')
    commands = next(action for action in parser()._actions if isinstance(action, argparse._SubParsersAction)).choices
    for command in commands:
        if command != 'serve' and not re.search(r'`' + re.escape(command) + r'(?:[ `])', reference):
            errors.append(f'Missing CLI documentation: {command}')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Documentation verified: {len(files)} Markdown files, {len(tools)} MCP tools, {len(commands)-1} CLI queries')


if __name__ == '__main__':
    asyncio.run(main())
