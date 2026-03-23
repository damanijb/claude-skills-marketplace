---
name: bloomberg-setup
description: Install and configure the Bloomberg MCP server — detects conda environments, checks Terminal connectivity, installs Python dependencies, patches .mcp.json with the correct Python path, and verifies the server works.
---

# Bloomberg MCP Server Setup

Run the following setup steps in order. Stop and report clearly if any step fails.

## Step 1: Detect Python Environment

Run the environment detector to find the best Python for Bloomberg:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/detect-python.py
```

This outputs JSON with the recommended Python path. Parse the result and note:
- `python_path` — the full path to use
- `env_type` — "conda" or "system"
- `env_name` — which conda environment (if applicable)
- `blpapi_installed` — whether blpapi is already available
- `all_environments` — every detected environment for the user to review

**If multiple conda environments have blpapi**, show the user the options and let them choose. The detector picks the best one automatically (active env with blpapi > any env with blpapi > system python).

**If no environment has blpapi yet**, recommend:
- If conda is available: create a dedicated env (`conda create -n bloomberg python=3.11 -y && conda activate bloomberg`)
- If no conda: use system Python (blpapi will be installed via pip in step 3)

## Step 2: Verify Bloomberg Terminal is Running

Using the detected Python path from step 1 (substitute `PYTHON_PATH` below):

```bash
PYTHON_PATH -c "
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

If this fails, tell the user to start Bloomberg Terminal and run `/bloomberg-setup` again.

## Step 3: Install Python Dependencies

Using the detected Python path:

**For conda environments:**
```bash
conda install -n ENV_NAME -c conda-forge blpapi xbbg -y
PYTHON_PATH -m pip install fastmcp>=2.0.0 polars-bloomberg>=0.5.0 polars>=1.0.0 matplotlib>=3.8.0 altair>=5.0.0 psutil>=5.9.0 pydantic>=2.0.0
```

**For system Python:**
```bash
PYTHON_PATH -m pip install fastmcp>=2.0.0 xbbg>=0.11.0 polars-bloomberg>=0.5.0 blpapi>=3.24.0 polars>=1.0.0 matplotlib>=3.8.0 altair>=5.0.0 psutil>=5.9.0 pydantic>=2.0.0
```

If `blpapi` fails via pip, suggest:
- Bloomberg's own index: `pip install blpapi --index-url=https://bcms.bloomberg.com/pip/simple/`
- Or conda: `conda install -c conda-forge blpapi`

## Step 4: Test Bloomberg API Connectivity

```bash
PYTHON_PATH -c "
from xbbg import blp
df = blp.bdp('IBM US Equity', 'PX_LAST')
if df is not None and not df.empty:
    print(f'Bloomberg API connected. IBM last price: {df.iloc[0,0]}')
else:
    print('ERROR: Bloomberg API returned empty data. Check Terminal is fully loaded.')
    exit(1)
"
```

## Step 5: Patch .mcp.json with Detected Python Path

**This is critical** — update the `.mcp.json` so the MCP server uses the correct Python.

Read `${CLAUDE_PLUGIN_ROOT}/.mcp.json` and replace the `"command": "python"` with the full path to the detected Python executable. For example, if the detected path is `C:/Users/user/.conda/envs/bloomberg/python.exe`, the `.mcp.json` should become:

```json
{
  "mcpServers": {
    "bloomberg": {
      "command": "C:/Users/user/.conda/envs/bloomberg/python.exe",
      "args": ["-m", "fastmcp", "run", "${CLAUDE_PLUGIN_ROOT}/server/server.py"],
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/server"
      }
    }
  }
}
```

Use forward slashes in the path even on Windows. Write the updated `.mcp.json` back to `${CLAUDE_PLUGIN_ROOT}/.mcp.json`.

## Step 6: Test the MCP Server

```bash
timeout 5 PYTHON_PATH -m fastmcp run ${CLAUDE_PLUGIN_ROOT}/server/server.py 2>&1 || true
```

## Completion

If all steps pass, report:

> Bloomberg MCP server is ready! You now have access to 10 Bloomberg tools:
> `bloomberg_status`, `bloomberg_bdp`, `bloomberg_bdh`, `bloomberg_bdib`, `bloomberg_bql`, `bloomberg_bql_build`, `bloomberg_bond_info`, `bloomberg_screen`, `bloomberg_field_search`, `bloomberg_chart`
>
> **Python**: {detected python path}
> **Environment**: {env_type} ({env_name})
>
> Try: "What's the current price of AAPL?" or "Show me SPY's performance over the last year"
>
> If using Claude Desktop, restart it once to pick up the MCP server registration.
