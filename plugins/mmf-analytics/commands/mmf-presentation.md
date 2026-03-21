---
description: Generate the full MMF monthly meeting presentation — fetches latest data, regenerates all charts, and builds a 16-slide PowerPoint deck ready for the investment review meeting.
allowed-tools: Bash, Read
argument-hint: [--fetch] [--no-charts] [--db path/to/mmf_holdings.db]
---

You are generating the MMF Monthly Investment Review presentation.

**Your goal:** Run the full analytics pipeline and produce a polished 16-slide PowerPoint deck, then give Damani a direct link.

## Step 1 — Parse arguments

Check `$ARGUMENTS` for any of:
- `--fetch` → include the SEC EDGAR data pull step
- `--no-charts` → skip chart regeneration (use existing PNGs)
- `--db <path>` → custom DB path

## Step 2 — Ask about data refresh (if --fetch not already specified)

If `--fetch` was NOT passed, ask the user ONE question:

> "Should I pull the latest N-MFP2 filings from SEC EDGAR before generating the presentation? This ensures the charts reflect the most recent data (adds ~2-3 minutes). Or skip and use current DB data?"

Wait for response. Map "yes/pull/fetch/update" → add `--fetch` flag.

## Step 3 — Run the presentation pipeline

The plugin scripts are installed at:
`/sessions/jolly-sharp-faraday/mnt/.local-plugins/marketplaces/local-desktop-app-uploads/mmf-analytics/skills/mmf-charting/scripts/`

However, use the source scripts from the tmp directory if available:
- Check: `ls /tmp/mmf-analytics/skills/mmf-charting/scripts/presentation_runner.py`
- If exists: use `/tmp/mmf-analytics/skills/mmf-charting/scripts/`
- Otherwise: use the installed plugin scripts dir

Build the command:
```bash
python3 <scripts_dir>/presentation_runner.py \
  --db /sessions/jolly-sharp-faraday/mnt/MMF_holdings/mmf_holdings.db \
  --out /sessions/jolly-sharp-faraday/mnt/MMF_holdings/MMF_Investment_Review.pptx \
  --charts-dir /tmp/mmf_charts \
  [--fetch if requested]
```

Run it and stream output. The script prints progress for each step.

## Step 4 — Confirm PPTX was created

Check that `/sessions/jolly-sharp-faraday/mnt/MMF_holdings/MMF_Investment_Review.pptx` exists.

If it does:
1. Tell the user the presentation is ready
2. Provide the link: `[View Presentation](computer:///sessions/jolly-sharp-faraday/mnt/MMF_holdings/MMF_Investment_Review.pptx)`
3. Give a 3-4 sentence summary of what's in the deck (report month, total AUM, slide count, highlights)

If it does NOT exist, show the error output and suggest re-running with `--fetch` if the issue looks data-related.

## Slide Overview (to help you summarize)

The deck contains 16 slides:
1. **Title** — Month/year, combined AUM, 4 fund tickers
2. **Agenda** — 4 agenda sections
3. **Section break** — Executive Summary
4. **Heatmap** — 8-metric cross-fund comparison table
5. **Section break** — Cross-Fund Overview
6. **AUM & Cash** — 12-month trend charts
7. **WAM & WAL** — Risk metric trends
8. **Month-over-Month** — Prior vs. current period bar charts
9. **Section break** — Fund Deep Dives
10–13. **Per Fund** (one slide each) — composition + maturity charts with 5 stat callouts
14. **Section break** — Issuer Concentration
15. **Top Issuers** — 2×2 grid of top-10 issuer charts per fund
16. **Data Notes** — Source, methodology, regulatory references
