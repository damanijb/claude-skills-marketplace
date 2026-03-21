---
description: Full per-fund deep dive: composition, maturity, flow, liquidity, HHI
allowed-tools: Bash, Read
argument-hint: <TICKER> [--db path/to/mmf_holdings.db]
---

Generate a full deep-dive analysis for a specific Government Money Market Fund.
Produces 5 charts: portfolio composition, maturity bucket distribution, AUM & flow, liquidity ratios, and HHI concentration.

## Interpreting Arguments

The argument `$ARGUMENTS` may be a raw ticker (e.g. `FRGXX`) or include flags.
Construct the command appropriately:
- If `$ARGUMENTS` is just a ticker symbol (FRGXX/GOFXX/MVRXX/BGSXX), run:
  ```
  python3 ${CLAUDE_PLUGIN_ROOT}/skills/mmf-charting/scripts/fund_deep_dive.py --ticker $ARGUMENTS
  ```
- If `$ARGUMENTS` includes flags like `--db`, pass them through as-is:
  ```
  python3 ${CLAUDE_PLUGIN_ROOT}/skills/mmf-charting/scripts/fund_deep_dive.py $ARGUMENTS
  ```
- If no ticker is specified, run for all 4 funds (omit `--ticker`):
  ```
  python3 ${CLAUDE_PLUGIN_ROOT}/skills/mmf-charting/scripts/fund_deep_dive.py
  ```

## Steps

1. Run the command above based on the arguments provided.

2. Parse all lines from stdout that start with `PNG:` to get the saved chart file paths.

3. For each PNG path found, use the Read tool to display the image inline in the chat.
   Display them in order: Composition → Maturity Buckets → AUM Flow → Liquidity → HHI.

4. After all 5 charts, provide a concise fund summary (4-5 sentences) covering:
   - Dominant portfolio category and any recent shifts
   - Maturity profile: is the fund short or long relative to peers?
   - AUM trend (growing/shrinking, notable MoM swings)
   - Liquidity: are daily and weekly minimums comfortably met?
   - Concentration: HHI level and whether it's increasing or decreasing

## Chart Descriptions

- **Composition**: Stacked bars showing % allocation to Agency Debt, Treasury Debt, Agency Repo, Treasury Repo, etc.
- **Maturity Buckets**: Stacked bars by WAL bucket (<=1d, 2-7d, 8-30d, 31-90d, 91-180d, 180+d)
- **AUM Flow**: Line chart of AUM with MoM change bars (green=inflow, red=outflow)
- **Liquidity**: Daily % and Weekly % of NAV with 10%/30% regulatory lines
- **HHI**: Herfindahl-Hirschman Index over time; zones: <1500 competitive, 1500-2500 moderate, >2500 concentrated
