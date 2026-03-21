---
description: Heatmap comparing all 4 MMF funds across 8 key metrics
allowed-tools: Bash, Read
argument-hint: [--db path/to/mmf_holdings.db]
---

Generate a color-coded heatmap comparing all 4 Government Money Market Funds
(FRGXX, GOFXX, MVRXX, BGSXX) side-by-side across 8 metrics for the latest reporting month.

## Steps

1. Run the heatmap script:
   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/mmf-charting/scripts/heatmap_chart.py $ARGUMENTS
   ```

2. Parse the `PNG:<path>` line from stdout.

3. Use the Read tool to display the image inline in chat.

4. After the chart, provide a 3-4 sentence interpretation covering:
   - Which fund looks strongest overall (most green cells)
   - Any red cells to flag (worst-performing metric for a fund)
   - Any regulatory concerns (⚠ warning symbols)
   - One notable insight about concentration or duration positioning

## Chart Layout

- **Rows**: FRGXX, GOFXX, MVRXX, BGSXX
- **Columns**: AUM ($B), WAM, WAL, Cash % NAV, Daily Liq %, Weekly Liq %, Top Issuer % NAV, HHI
- **Color logic**: per-column relative ranking
  - Green = favorable (↑ better for liquidity, ↓ better for duration/concentration)
  - Red = unfavorable
  - Blue = neutral (AUM, Cash % — no directional judgment)
- **⚠ icon**: appears if a fund is below the regulatory minimum (10% daily, 30% weekly)

## Notes
- Default DB: `/sessions/jolly-sharp-faraday/mnt/MMF_holdings/mmf_holdings.db`
- Colors are relative within each column — a green cell means best among the 4 funds, not an absolute good
