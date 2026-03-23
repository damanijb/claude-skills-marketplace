---
name: bloomberg-setup
description: Set up the Bloomberg MCP server — detect Bloomberg Terminal, install Python dependencies (blpapi, xbbg, polars-bloomberg, fastmcp), verify connectivity, and troubleshoot common issues. Use when Bloomberg tools are unavailable, after first plugin install, or when bloomberg_status returns errors.
version: 1.0.0
metadata:
  filePattern: "**/bloomberg*/**,**/mcp-bloomberg/**"
  bashPattern: "pip install.*blpapi|pip install.*xbbg|bloomberg|fastmcp"
---

# Bloomberg MCP Server Setup

This skill guides first-time setup and troubleshooting of the Bloomberg MCP server.

## Prerequisites

Before starting, the user's machine MUST have:
1. **Bloomberg Terminal** installed and running (wintrv.exe visible in Task Manager)
2. **Python 3.10+** available on PATH
3. **C++ Build Tools** (required by blpapi) — Visual Studio Build Tools on Windows

## Setup Steps

### Step 1: Check Bloomberg Terminal

Run this command to verify Bloomberg processes are running:

```bash
python -c "import psutil; bbg = [p.name() for p in psutil.process_iter(['name']) if p.info['name'] and p.info['name'].lower() in {'wintrv.exe','bbcomm.exe','bblauncher.exe','bbg.exe'}]; print(f'Bloomberg processes: {bbg}' if bbg else 'WARNING: No Bloomberg Terminal processes detected. Please start Bloomberg Terminal first.')"
```

If no processes found, tell the user to:
- Open Bloomberg Terminal (WIN+R → `wintrv`)
- Log in with their Bloomberg credentials
- Wait for the terminal to fully load before proceeding

### Step 2: Install Python Dependencies

Install all required packages. The `blpapi` package requires the Bloomberg C++ SDK.

```bash
pip install fastmcp>=2.0.0 xbbg>=0.11.0 polars-bloomberg>=0.5.0 blpapi>=3.24.0 polars>=1.0.0 matplotlib>=3.8.0 altair>=5.0.0 psutil>=5.9.0 pydantic>=2.0.0
```

**If blpapi fails to install:**
1. Download the Bloomberg C++ SDK from the Bloomberg SAPI website
2. Set `BLPAPI_ROOT` environment variable to the SDK path
3. Retry: `pip install blpapi`

**Alternative for conda users:**
```bash
conda install -c conda-forge blpapi xbbg
pip install fastmcp polars-bloomberg polars matplotlib altair psutil pydantic
```

### Step 3: Verify Connectivity

Test that the Bloomberg API connection works:

```bash
python -c "from xbbg import blp; df = blp.bdp('IBM US Equity', 'PX_LAST'); print(f'SUCCESS: IBM last price = {df.iloc[0,0]}' if not df.empty else 'FAILED: Empty response')"
```

### Step 4: Test the MCP Server

Start the server directly to verify it loads:

```bash
python -m fastmcp run ${CLAUDE_PLUGIN_ROOT}/server/server.py
```

If successful, you'll see the FastMCP startup message. Press Ctrl+C to stop.

## Troubleshooting

### "blpapi not found" or import errors
- Ensure Bloomberg Terminal is running BEFORE importing blpapi
- The Terminal must be logged in (not just the splash screen)
- Try: `python -c "import blpapi; print(blpapi.__version__)"`

### "Connection refused" or timeout errors
- Bloomberg Terminal must be on the SAME machine (remote connections need B-PIPE)
- Check firewall isn't blocking localhost:8194
- Restart Bloomberg Terminal and try again

### "lifespan_context" error in Claude Desktop
- This means the MCP server crashed during startup
- Fully quit Claude Desktop (system tray → Exit)
- Restart Claude Desktop
- The MCP server will re-initialize on first tool call

### Server starts but tools return empty data
- Verify your Bloomberg subscription includes the data you're requesting
- Some fields require specific entitlements (e.g., real-time vs delayed)
- Try a simple test: `bloomberg_bdp(securities=["IBM US Equity"], fields=["PX_LAST"])`

### conda environment issues
- Run `python ${CLAUDE_PLUGIN_ROOT}/scripts/detect-python.py` to find all available environments
- The `/bloomberg-setup` command auto-detects conda and patches `.mcp.json` with the correct Python path
- If auto-detection picked the wrong env, edit `.mcp.json` manually:
  ```json
  "command": "C:/Users/you/.conda/envs/bloomberg/python.exe"
  ```
- To create a dedicated environment:
  ```bash
  conda create -n bloomberg python=3.11 -y
  conda activate bloomberg
  conda install -c conda-forge blpapi xbbg -y
  pip install fastmcp polars-bloomberg polars matplotlib altair psutil pydantic
  ```

### .mcp.json shows "python" but wrong Python runs
- This happens when the system `python` points to a different environment
- Fix: run `/bloomberg-setup` — it detects the right Python and patches `.mcp.json`
- Or manually set the full path in `.mcp.json` → `"command": "/full/path/to/python"`

## For Team Distribution

When sharing this plugin with teammates:

1. They clone the repo: `git clone <repo-url>`
2. They install the plugin: `claude plugins add ./BloombergMCP`
3. They run `/bloomberg-setup` to install dependencies
4. They restart Claude Code — Bloomberg tools are ready

No manual config editing required. The `.mcp.json` handles server registration automatically.
