---
description: Top 10 issuers by % of NAV for one or all MMF funds
allowed-tools: Bash, Read
argument-hint: [TICKER] [--db path/to/mmf_holdings.db]
---

Generate a Top 10 issuer horizontal bar chart showing % of NAV concentration at latest reporting date.
If a ticker is specified, shows that fund only. Otherwise shows all 4 funds.

## Interpreting Arguments

- If `$ARGUMENTS` is a ticker (FRGXX/GOFXX/MVRXX/BGSXX):
  ```
  python3 ${CLAUDE_PLUGIN_ROOT}/skills/mmf-charting/scripts/top_issuers.py --ticker $ARGUMENTS
  ```
- If `$ARGUMENTS` includes flags, pass through as-is:
  ```
  python3 ${CLAUDE_PLUGIN_ROOT}/skills/mmf-charting/scripts/top_issuers.py $ARGUMENTS
  ```
- If no ticker provided, run for all 4 funds:
  ```
  python3 ${CLAUDE_PLUGIN_ROOT}/skills/mmf-charting/scripts/top_issuers.py
  ```

## Steps

1. Run the appropriate command above.

2. Parse all lines from stdout that start with `PNG:` to get saved chart paths.

3. For each PNG path found, use the Read tool to display the image inline.

4. After all charts, provide a brief concentration note:
   - Name the top 3 issuers and their % of NAV
   - Note if top-5 concentration exceeds 50% of NAV (flag as elevated)
   - Identify if any single issuer exceeds 10% (notable concentration)
