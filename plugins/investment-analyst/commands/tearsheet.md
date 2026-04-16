---
description: Update a quarterly issuer tearsheet — pull earnings writeup from Outlook, enrich with Bloomberg BQL economic context, inject into Excel template via COM, export PDF to quarterly archive folder, and update Obsidian vault. Covers all 44 SBC covered issuers including fiscal offset handling for Canadian banks, Toyota, Visa, and other non-calendar-year issuers.
allowed-tools: Bash, Read, Write, Edit, Agent, TodoWrite, AskUserQuestion, mcp__bloomberg__bloomberg_bql, mcp__bloomberg__bloomberg_bdp, mcp__desktop-commander__read_file, mcp__desktop-commander__write_file, mcp__desktop-commander__edit_block, mcp__desktop-commander__list_directory
argument-hint: "[issuer] [quarter] — e.g., Citibank 1Q26 | JP Morgan 1Q26 | BNP Paribas 1Q26"
---

Load and follow the full workflow in:
`${CLAUDE_PLUGIN_ROOT}/skills/tearsheet/SKILL.md`

**Arguments provided:** $ARGUMENTS

Parse `$ARGUMENTS` to extract:
- **issuer** — the covered issuer name (e.g., "Citibank", "JP Morgan", "Bank of America")
- **quarter** — the calendar quarter label (e.g., "1Q26", "2Q26")

If no arguments are provided, use AskUserQuestion to ask which issuer and quarter to process.

Refer to `${CLAUDE_PLUGIN_ROOT}/skills/tearsheet/references/issuer-config.md` for the
complete issuer → template mapping, CDS tickers, fiscal offset details, and vault paths.
