# Connect your agent

Create a personal key at https://mcp.xhunt.ai/account. Configure it privately in your client. Account availability depends on the auth-billing deployment and enabled identity providers. Direct remote MCP is the shortest setup; local stdio adds credit-aware defaults, CLI and the `get_usage` tool.

## Claude Code: direct remote MCP

```bash
claude mcp add --transport http influence https://mcp.xhunt.ai/mcp \
  --header "Authorization: Bearer YOUR_XHUNT_API_KEY"
```

The command configures this connection only. It does not grant the server file or shell permissions. Read your client’s approval settings. Start with: “Read Influence capabilities, then show at most 5 AI creators on YouTube with source time.”

## Cursor: direct remote MCP

Merge this entry into `~/.cursor/mcp.json` or your project’s `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "influence": {
      "url": "https://mcp.xhunt.ai/mcp",
      "headers": {"Authorization": "Bearer YOUR_XHUNT_API_KEY"}
    }
  }
}
```

Keep project configurations containing a key out of Git. Use client secret storage or environment interpolation where your installed client version supports it.

## VS Code: remote MCP

Merge into your MCP configuration (for a project, `.vscode/mcp.json`):

```json
{
  "inputs": [{"type": "promptString", "id": "xhunt-key", "description": "XHunt API key", "password": true}],
  "servers": {
    "influence": {
      "type": "http",
      "url": "https://mcp.xhunt.ai/mcp",
      "headers": {"Authorization": "Bearer ${input:xhunt-key}"}
    }
  }
}
```

## Claude Desktop, Cursor, Windsurf: local stdio

Install Python 3.10+ and uv. Keep a local checkout of this repository and run `uv sync --locked` in it. Use its **absolute path** in this configuration:

```json
{
  "mcpServers": {
    "influence": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/influence-client", "run", "--locked", "influence-client", "serve"],
      "env": {"XHUNT_API_KEY": "YOUR_XHUNT_API_KEY"}
    }
  }
}
```

- Claude Desktop: edit its `claude_desktop_config.json`.
- Cursor: `~/.cursor/mcp.json`.
- Windsurf: `~/.codeium/windsurf/mcp_config.json`.
- Other stdio clients: command `uv`, arguments above, private environment variable `XHUNT_API_KEY`.

These are standard protocol configurations, not a claim that every client release has been manually verified. Local MCP protocol and the hosted service are verified separately; see [verification](../docs/verification.md).

## Skills / OpenClaw

Use [skills/influence/SKILL.md](../skills/influence/SKILL.md) with an agent that supports local Skills. For OpenClaw, from the repository checkout:

```bash
mkdir -p "$HOME/.openclaw/skills"
cp -r skills/influence "$HOME/.openclaw/skills/"
```

Configure `XHUNT_API_KEY` in the agent’s private environment and set `INFLUENCE_CLIENT_DIR` to the absolute repository path. Copying a Skill does not install Python dependencies or provide a key. The Skill uses the CLI and does not require the local MCP server to be running.

## Configuration

| Variable | Default | Meaning |
| --- | --- | --- |
| `XHUNT_API_KEY` | unset | Required for data and usage; not needed for public capabilities |
| `XHUNT_BASE_URL` | `https://mcp.xhunt.ai` | Trusted API origin; HTTPS required except localhost |
| `INFLUENCE_CLIENT_DIR` | unset | Repository path used by the copied CLI Skill |

`.env` files are not loaded automatically. Export values or use the MCP client’s environment configuration. The client never follows redirects with credentials.

If a network timeout occurs, check before retrying a data request: it may have reached the server and consumed credits. The client does not retry automatically.
