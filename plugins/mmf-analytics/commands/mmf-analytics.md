---
description: Run the full MMF analytics suite — all charts for all 4 funds
allowed-tools: Bash, Read
argument-hint: [--db path/to/mmf_holdings.db] [--days 365]
---

Run the complete MMF analytics suite, producing all charts across all 4 funds:
cross-fund comparisons, latest-month summary, per-fund deep dives, and top-issuer charts.

## Steps

1. Let the user know you're starting the full analytics run (may take 30-60 seconds for Datawrapper).

2. Run each script sequentially, capturing output. Pass `$ARGUMENTS` to each script:
   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/mmf-charting/scripts/cross_fund_charts.py $ARGUMENTS
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/mmf-charting/scripts/summary_charts.py $ARGUMENTS
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/mmf-charting/scripts/fund_deep_dive.py $ARGUMENTS
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/mmf-charting/scripts/top_issuers.py $ARGUMENTS
   ```

3. After each script completes, collect all `PNG:<path>` lines from its stdout.
   Use the Read tool to display each PNG inline, grouping by section:
   - **Section 1: Cross-Fund Comparison** (4 charts)
   - **Section 2: Latest Month Summary** (1-6 charts)
   - **Section 3: Per-Fund Deep Dives** (5 charts × up to 4 funds)
   - **Section 4: Top Issuers** (1 chart × up to 4 funds)

4. After all charts are displayed, produce a 1-page executive summary covering:
   - Overall AUM and flows across the 4 funds
   - Duration positioning (WAM/WAL trends)
   - Liquidity compliance status (all funds vs. 10%/30% minimums)
   - Portfolio composition shifts (notable category changes)
   - Concentration highlights (top issuers, HHI)
   - Any funds of concern based on the data shown

## Notes
- Default DB: `/sessions/jolly-sharp-faraday/mnt/MMF_holdings/mmf_holdings.db`
- Default lookback: 365 days
- Datawrapper charts will be published and exported as PNG; matplotlib is the fallback
- All charts saved to `/tmp/mmf_charts/`
