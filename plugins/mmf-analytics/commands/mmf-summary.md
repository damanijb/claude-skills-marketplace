---
description: Latest-month snapshot bar charts for all 4 MMF funds
allowed-tools: Bash, Read
argument-hint: [--db path/to/mmf_holdings.db]
---

Generate latest-month summary charts for all 4 Government Money Market Funds (FRGXX, GOFXX, MVRXX, BGSXX).

## Steps

1. Run the summary charts script:
   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/mmf-charting/scripts/summary_charts.py $ARGUMENTS
   ```

2. Parse all lines from stdout that start with `PNG:` to get the saved chart file paths.

3. For each PNG path found, use the Read tool to display the image inline in the chat.

4. After showing all charts, provide a brief 2-3 sentence narrative covering:
   - Which fund has the highest/lowest AUM
   - Whether all funds meet the 10% daily liquidity and 30% weekly liquidity minimums
   - Any notable outliers in WAM or WAL

## Notes
- If no `--db` argument is passed, the script defaults to `/sessions/jolly-sharp-faraday/mnt/MMF_holdings/mmf_holdings.db`
- Charts use Datawrapper if available; otherwise clean matplotlib (white background, no gridlines)
- The summary chart grid shows AUM ($B), WAM, WAL, Cash% of NAV, Daily Liq%, and Weekly Liq%
