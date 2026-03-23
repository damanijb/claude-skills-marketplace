"""Wrapper to run the Bloomberg MCP server via stdio transport.

Claude Desktop and Claude Code both need a script that runs directly
with `python run_server.py` (not `python -m fastmcp run`) because
fastmcp lacks a __main__.py module.
"""
import sys
from pathlib import Path

# Ensure lib/ is on path for extra dependencies (fastmcp, xbbg, polars, etc.)
lib_path = str(Path(__file__).parent.parent / "lib")
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

from server import mcp

if __name__ == "__main__":
    mcp.run(transport="stdio")
