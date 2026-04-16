---
description: Generate a CreditSights-style quarterly credit analysis report with embedded charts, earnings snapshot table, capital waterfall, segment analysis, and monitoring flags for any SBC Treasury covered issuer.
allowed-tools: Bash, Read, Write, Edit, Agent, TodoWrite, AskUserQuestion, mcp__desktop-commander__read_file, mcp__desktop-commander__write_file, mcp__desktop-commander__list_directory, mcp__desktop-commander__start_process, mcp__desktop-commander__read_process_output
argument-hint: "[issuer] [quarter] — e.g., JPM 1Q26 | Citigroup 1Q26 | BNP Paribas 1Q26"
---

Load and follow the full workflow in:
`${CLAUDE_PLUGIN_ROOT}/skills/credit-report/SKILL.md`

For chart and report format specifications, refer to:
`${CLAUDE_PLUGIN_ROOT}/skills/credit-report/references/report-format.md`

**Arguments provided:** $ARGUMENTS

Parse `$ARGUMENTS` to extract:
- **issuer** — covered issuer name or ticker (e.g., "JPM", "Citigroup", "Bank of America", "BNP Paribas")
- **quarter** — calendar quarter label (e.g., "1Q26", "2Q26")

If no arguments are provided, use AskUserQuestion to ask which issuer and quarter to process.

After generating, present:
1. Link to the HTML report (primary deliverable)
2. Link to the DOCX companion
3. One-paragraph summary of the recommendation rationale and key monitoring flags
