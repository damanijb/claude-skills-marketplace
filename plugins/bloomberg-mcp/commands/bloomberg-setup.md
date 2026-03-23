---
name: bloomberg-setup
description: Install and configure the Bloomberg MCP server — uses Bloomberg's own BQuant Python (blpapi pre-installed), installs extra deps to plugin-local lib/, verifies connectivity.
---

# Bloomberg MCP Server Setup

Uses Bloomberg's BQuant Python at `C:/blp/bqnt/environments/bqnt-3/python.exe` which already has `blpapi` installed. Extra dependencies are installed into the plugin's own `lib/` directory to avoid modifying Bloomberg's managed environment.

Run the following steps in order. Stop and report clearly if any step fails.

## Step 1: Verify Bloomberg Terminal is Running

```bash
"C:/blp/bqnt/environments/bqnt-3/python.exe" -c "
import psutil
bbg_names = {'wintrv.exe', 'bbcomm.exe', 'bblauncher.exe', 'bbg.exe'}
found = [p.info['name'] for p in psutil.process_iter(['name']) if (p.info['name'] or '').lower() in bbg_names]
if found:
    print(f'Bloomberg Terminal detected: {found}')
else:
    print('ERROR: Bloomberg Terminal is not running.')
    print('Please start Bloomberg Terminal (WIN+R -> wintrv) and log in before continuing.')
    exit(1)
"
```

If BQuant Python is not found at `C:/blp/bqnt/environments/bqnt-3/python.exe`, check:
- Is Bloomberg Terminal installed? The BQuant environment ships with it.
- Alternative paths: `C:/blp/bqnt/environments/bqnt-2/python.exe` or check `C:/blp/bqnt/environments/` for available versions.
- If no BQuant environment exists, fall back to any Python with `blpapi` installed and update `.mcp.json` accordingly.

## Step 2: Install Extra Dependencies to Plugin lib/

Install the packages Bloomberg's Python is missing into a local `lib/` directory:

```bash
"C:/blp/bqnt/environments/bqnt-3/python.exe" -m pip install --target "${CLAUDE_PLUGIN_ROOT}/lib" --upgrade --no-deps fastmcp xbbg polars-bloomberg polars pydantic pydantic-core altair anyio httpx httpx-sse sniffio certifi idna h11 starlette typing-extensions annotated-types uvicorn click jsonschema narwhals toolz jinja2 markupsafe packaging jsonschema-specifications referencing rpds-py attrs
```

**Why `--no-deps` with explicit packages?** We list transitive deps explicitly to avoid `--target` pulling packages that Bloomberg's Python already has (like `numpy`, `pandas`). This keeps `lib/` small and avoids version conflicts.

If any package fails, retry without `--no-deps`:
```bash
"C:/blp/bqnt/environments/bqnt-3/python.exe" -m pip install --target "${CLAUDE_PLUGIN_ROOT}/lib" fastmcp xbbg polars-bloomberg polars pydantic altair
```

## Step 3: Verify the lib/ Directory Works

```bash
"C:/blp/bqnt/environments/bqnt-3/python.exe" -c "
import sys
sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/lib')
import fastmcp; print(f'fastmcp: {fastmcp.__version__}')
import xbbg; print(f'xbbg: ok')
import pydantic; print(f'pydantic: {pydantic.__version__}')
import polars; print(f'polars: {polars.__version__}')
import blpapi; print(f'blpapi: {blpapi.__version__} (from Bloomberg)')
print('All dependencies verified.')
"
```

## Step 4: Test Bloomberg API Connectivity

```bash
"C:/blp/bqnt/environments/bqnt-3/python.exe" -c "
import sys; sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/lib')
from xbbg import blp
df = blp.bdp('IBM US Equity', 'PX_LAST')
if df is not None and not df.empty:
    print(f'Bloomberg API connected. IBM last price: {df.iloc[0,0]}')
else:
    print('ERROR: Bloomberg API returned empty data. Check Terminal is fully loaded.')
    exit(1)
"
```

## Step 5: Test the MCP Server

```bash
timeout 5 "C:/blp/bqnt/environments/bqnt-3/python.exe" -c "
import sys; sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/lib'); sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/server')
from server import mcp
print('MCP server loaded successfully with', len(mcp._tool_manager._tools), 'tools')
" 2>&1 || true
```

## Completion

If all steps pass, report:

> Bloomberg MCP server is ready! You now have access to 10 Bloomberg tools:
> `bloomberg_status`, `bloomberg_bdp`, `bloomberg_bdh`, `bloomberg_bdib`, `bloomberg_bql`, `bloomberg_bql_build`, `bloomberg_bond_info`, `bloomberg_screen`, `bloomberg_field_search`, `bloomberg_chart`
>
> **Python**: `C:/blp/bqnt/environments/bqnt-3/python.exe` (Bloomberg BQuant)
> **blpapi**: pre-installed by Bloomberg
> **Extra deps**: installed to `${CLAUDE_PLUGIN_ROOT}/lib/`
>
> Try: "What's the current price of AAPL?" or "Show me SPY's performance over the last year"
>
> Restart Claude Code to pick up the MCP server registration.
