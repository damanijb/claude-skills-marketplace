---
description: Cross-fund time series: AUM, Cash%, WAM, WAL for all 4 MMFs
allowed-tools: Bash, Read
argument-hint: [--db path/to/mmf_holdings.db] [--days 365]
---

Generate four time-series line charts comparing all 4 Government Money Market Funds over the past 12 months.
Charts produced: AUM ($B), Cash % of NAV, Weighted Average Maturity, Weighted Average Life.

## Steps

1. Run the cross-fund charts script:
   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/mmf-charting/scripts/cross_fund_charts.py $ARGUMENTS
   ```

2. Parse all lines from stdout that start with `PNG:` to get the saved chart file paths.

3. For each PNG path found, use the Read tool to display the image inline in the chat.

4. After displaying all 4 charts, provide a brief narrative (3-4 sentences) covering:
   - AUM trend: which fund is growing or shrinking?
   - WAM/WAL trend: are funds shortening or extending duration?
   - Cash % trend: any notable shifts in cash allocation?
   - Any divergence between funds worth highlighting

## Notes
- The 4 charts (one per metric) each show all 4 tickers as separate lines
- Color coding: FRGXX=#1f77b4 (blue), GOFXX=#ff7f0e (orange), MVRXX=#2ca02c (green), BGSXX=#d62728 (red)
- Default lookback is 365 days; override with `--days N`
