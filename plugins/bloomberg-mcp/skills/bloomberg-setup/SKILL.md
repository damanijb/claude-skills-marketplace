---
name: bloomberg-setup
description: Set up the Bloomberg MCP server — uses Bloomberg's BQuant Python (blpapi pre-installed), installs extra deps to plugin-local lib/, verifies connectivity, and troubleshoots common issues. Use when Bloomberg tools are unavailable, after first plugin install, or when bloomberg_status returns errors.
version: 1.0.0
metadata:
  filePattern: "**/bloomberg*/**,**/mcp-bloomberg/**"
  bashPattern: "pip install.*blpapi|pip install.*xbbg|bloomberg|fastmcp"
---

# Bloomberg MCP Server Setup

This skill guides first-time setup and troubleshooting of the Bloomberg MCP server.

## Architecture

The plugin uses **Bloomberg's own BQuant Python** (`C:/blp/bqnt/environments/bqnt-3/python.exe`) which ships with every Bloomberg Terminal installation. This Python already has `blpapi` installed.

Extra dependencies (`fastmcp`, `xbbg`, `polars-bloomberg`, `polars`, `pydantic`) are installed into a **plugin-local `lib/` directory** via `pip install --target`. This avoids modifying Bloomberg's managed environment and survives Bloomberg updates.

The server launches via `run_server.py` — a thin wrapper that adds `lib/` to `sys.path` and calls `mcp.run(transport="stdio")`. This is necessary because `python -m fastmcp run` does not work (fastmcp lacks a `__main__.py`).

The `.mcp.json` is simple:
```json
{
  "command": "C:/blp/bqnt/environments/bqnt-3/python.exe",
  "args": ["${CLAUDE_PLUGIN_ROOT}/server/run_server.py"]
}
```

## Prerequisites

1. **Bloomberg Terminal** installed and running (wintrv.exe visible in Task Manager)
2. **BQuant environment** at `C:/blp/bqnt/environments/bqnt-3/` (standard Bloomberg install path)

That's it. No conda, no system Python, no C++ build tools needed.

## Setup via Command

Run `/bloomberg-setup` for guided installation. The command:
1. Verifies Bloomberg Terminal is running
2. Installs extra deps to `${CLAUDE_PLUGIN_ROOT}/lib/` (polars first with deps, then everything else with `--no-deps`)
3. Verifies all imports work
4. Tests API connectivity
5. Tests MCP server launches on stdio

## Dependency Install Strategy

fastmcp 3.1.x has a large transitive dependency tree. The setup uses two passes:

1. **`polars` with full deps** — needs its native `polars-runtime-32` binary wheel
2. **Everything else with `--no-deps`** — explicit list of ~60 packages to avoid pulling packages Bloomberg's Python already has (numpy, pandas, scipy, etc.)

Key gotchas that the dependency list accounts for:
- `pydantic` requires `pydantic-core` at an exact version — if upgraded separately they can mismatch
- `pydantic` 2.12+ requires `typing-inspection` (new dependency)
- `pydantic-settings` and `python-dotenv` are required by fastmcp
- `rich`, `pygments`, `markdown-it-py`, `mdurl` are required for fastmcp's logging
- `opentelemetry-api`, `opentelemetry-sdk`, `opentelemetry-semantic-conventions` are required for fastmcp's telemetry
- `mcp` (the MCP SDK), `httpcore`, `sse-starlette`, `python-multipart` are required for the protocol layer
- `pyarrow` is required by xbbg
- `pywin32` is required by the MCP SDK on Windows

## Troubleshooting

### BQuant Python not found at expected path
- Check `C:/blp/bqnt/environments/` for available versions (bqnt-2, bqnt-3, etc.)
- If a different version exists, update `.mcp.json` command to match
- If no BQuant environment exists, Bloomberg Terminal may need the BQuant feature enabled

### "blpapi not found" or import errors
- BQuant Python should already have blpapi — verify: `"C:/blp/bqnt/environments/bqnt-3/python.exe" -c "import blpapi; print(blpapi.__version__)"`
- If missing, Bloomberg Terminal installation may be incomplete

### "No module named 'fastmcp'" when MCP server starts
- The `lib/` directory hasn't been populated yet — run `/bloomberg-setup`
- Or manually: `"C:/blp/bqnt/environments/bqnt-3/python.exe" -m pip install --target "${CLAUDE_PLUGIN_ROOT}/lib" fastmcp xbbg polars-bloomberg polars pydantic altair`

### "No module named fastmcp.__main__" / "cannot be directly executed"
- This means someone tried `python -m fastmcp run` — fastmcp doesn't support that
- The server must be launched via `run_server.py` which calls `mcp.run()` directly
- Check `.mcp.json` uses `run_server.py`, not `-m fastmcp run`

### pydantic / pydantic-core version mismatch
- pydantic pins an exact pydantic-core version. If they're installed at different times, they can mismatch
- Fix: `pip install --target lib --upgrade --no-deps pydantic pydantic-core` (install together)

### "Connection refused" or timeout errors
- Bloomberg Terminal must be on the SAME machine (remote needs B-PIPE)
- Check firewall isn't blocking localhost:8194
- Restart Bloomberg Terminal and try again

### "'NoneType' object has no attribute 'lifespan_context'"
- This is a FastMCP/xbbg issue where the Bloomberg client isn't initialized in the async context
- Usually occurs with `bloomberg_screen` and `bloomberg_bdh` tools
- `bloomberg_bdp`, `bloomberg_bql`, and `bloomberg_field_search` typically work fine
- Workaround: use `bloomberg_bql` for screening instead of `bloomberg_screen`

### Server disconnects after a few seconds in Claude Desktop
- The server process exits because Claude Desktop closes and reopens the transport during initialization
- This is normal — Claude Desktop will reconnect automatically
- If tools list loads but then disconnects, the server is working; it reconnects on first tool call

### Server starts but tools return empty data
- Verify your Bloomberg subscription covers the requested data
- Some fields require specific entitlements (real-time vs delayed)
- Test: `bloomberg_bdp(securities=["IBM US Equity"], fields=["PX_LAST"])`

### Version conflicts between lib/ and Bloomberg's packages
- If you see import errors after setup, clear and reinstall:
  ```bash
  rm -rf "${CLAUDE_PLUGIN_ROOT}/lib"
  /bloomberg-setup
  ```
- The `--no-deps` install strategy prevents most conflicts

## For Team Distribution

When sharing this plugin with teammates:

1. They clone the marketplace repo (or just the `bloomberg-mcp` plugin directory)
2. They install the plugin: `claude plugins add ./plugins/bloomberg-mcp`
3. They run `/bloomberg-setup` to install extra deps to `lib/`
4. They restart Claude Code — Bloomberg tools are ready

**Why this works on any Bloomberg machine:**
- `C:/blp/bqnt/environments/bqnt-3/python.exe` is the same path on every Bloomberg Terminal
- `blpapi` is pre-installed by Bloomberg — no pip/conda install needed
- Extra deps go to a plugin-local directory — no environment configuration
- `.mcp.json` uses `${CLAUDE_PLUGIN_ROOT}` for portable paths
- `run_server.py` handles `sys.path` setup — no PYTHONPATH env var needed
