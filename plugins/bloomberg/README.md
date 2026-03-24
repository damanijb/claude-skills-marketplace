# Bloomberg Plugin for Claude Code

Query Bloomberg market data directly from Claude Code using BQL (Bloomberg Query Language).

## Prerequisites

- **Bloomberg Terminal** running and logged in
- **Node.js** 16+ on PATH
- **Bloomberg bqnt-3 Python** at `C:\blp\bqnt\environments\bqnt-3\python.exe` (standard on every terminal)

## Installation

```bash
claude plugin add /path/to/bloomberg-plugin
```

Or clone/copy this directory and add it as a local plugin.

## What you get

### MCP Tool: `bql_query`
Run any BQL query and get JSON results. Claude can call this tool directly.

### MCP Tool: `bql_examples`
Get verified example queries by domain — teaches Claude correct BQL syntax before querying.

### Skill: `bloomberg`
Comprehensive BQL reference docs (16 domain files, 27 verified test queries) that teach Claude
how to write correct BQL. Covers equity, fixed income, credit, CDS, curves, funds, returns, and more.

## Usage

Just ask Claude naturally:
- "Get Apple's stock price for the past month"
- "Screen S&P 500 for stocks with PE under 15 and market cap over 50B"
- "Find AA-rated bonds with duration under 2 and yield over 4%"
- "Show me JPM's 5-year CDS spread history"
- "Get the US Treasury yield curve"

## Architecture

```
Claude Code
  ├── Skill (SKILL.md + references/) → teaches correct BQL syntax
  └── MCP Server (Node.js + stdio)
        └── bql_worker.py (bqnt-3 Python) → bql.Service() → Bloomberg Terminal
```
