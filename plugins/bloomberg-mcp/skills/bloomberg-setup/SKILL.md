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

Extra dependencies (`fastmcp`, `xbbg`, `polars-bloomberg`, `polars`, `pydantic`, `altair`) are installed into a **plugin-local `lib/` directory** via `pip install --target`. This avoids modifying Bloomberg's managed environment and survives Bloomberg updates.

The `.mcp.json` sets `PYTHONPATH` to include both `lib/` and `server/`:
```json
{
  "command": "C:/blp/bqnt/environments/bqnt-3/python.exe",
  "env": { "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/lib;${CLAUDE_PLUGIN_ROOT}/server" }
}
```

## Prerequisites

1. **Bloomberg Terminal** installed and running (wintrv.exe visible in Task Manager)
2. **BQuant environment** at `C:/blp/bqnt/environments/bqnt-3/` (standard Bloomberg install path)

That's it. No conda, no system Python, no C++ build tools needed.

## Setup via Command

Run `/bloomberg-setup` for guided installation. The command:
1. Verifies Bloomberg Terminal is running
2. Installs extra deps to `${CLAUDE_PLUGIN_ROOT}/lib/`
3. Tests API connectivity
4. Tests MCP server loads

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

### "Connection refused" or timeout errors
- Bloomberg Terminal must be on the SAME machine (remote needs B-PIPE)
- Check firewall isn't blocking localhost:8194
- Restart Bloomberg Terminal and try again

### "lifespan_context" error in Claude Desktop
- MCP server crashed during startup — fully quit and restart Claude Desktop
- The server re-initializes on first tool call

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
