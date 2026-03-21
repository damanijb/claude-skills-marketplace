# MMF Analytics Plugin

Automated analytics and clean Datawrapper charts for four Government Money Market Funds:
**FRGXX** (Fidelity), **GOFXX** (Goldman), **MVRXX** (Morgan Stanley), **BGSXX** (BlackRock).

Data source: SEC EDGAR N-MFP2 filings stored in `mmf_holdings.db` (SQLite).

---

## Commands

| Command | What it does |
|---------|-------------|
| `/mmf-summary` | Latest-month bar charts: AUM, WAM, WAL, Cash%, Daily Liq%, Weekly Liq% |
| `/mmf-cross-fund` | 12-month line charts comparing all 4 funds across key metrics |
| `/mmf-fund <TICKER>` | Full deep dive for one fund (or all 4 if no ticker given) |
| `/mmf-issuers [TICKER]` | Top 10 issuers by % of NAV at latest date |
| `/mmf-analytics` | Run the complete suite — all charts + executive summary |

### Examples

```
/mmf-summary
/mmf-cross-fund --days 180
/mmf-fund FRGXX
/mmf-fund GOFXX --db /path/to/custom.db
/mmf-issuers BGSXX
/mmf-analytics
```

---

## Setup

### 1. Install Dependencies

```bash
pip install datawrapper pandas numpy matplotlib --break-system-packages
```

### 2. Database

Default database path: `/sessions/jolly-sharp-faraday/mnt/MMF_holdings/mmf_holdings.db`

Override with `--db <path>` on any command, or set the environment variable:
```bash
export MMF_DB_PATH=/your/path/to/mmf_holdings.db
```

### 3. Datawrapper (optional but recommended)

The Datawrapper API token is pre-configured in `skills/mmf-charting/scripts/chart_utils.py`.
Charts automatically fall back to clean matplotlib (white background, no gridlines) if Datawrapper is unavailable.

---

## Chart Output

All PNGs are saved to `/tmp/mmf_charts/` by default. Override with `--out <dir>`.
Charts display inline in chat immediately after generation via the Read tool.

---

## Chart Types

### Cross-Fund (`/mmf-cross-fund`)
Four line charts — one per metric — each showing all 4 fund tickers over 12 months:
- AUM ($B)
- Cash % of NAV
- Weighted Average Maturity (WAM, days)
- Weighted Average Life (WAL, days)

### Summary (`/mmf-summary`)
Six bar charts showing latest-month values for all 4 funds:
- AUM, WAM, WAL, Cash%, Daily Liquid %, Weekly Liquid %
- Regulatory reference lines at 10% (daily) and 30% (weekly)

### Fund Deep Dive (`/mmf-fund`)
Five charts per fund:
1. **Composition** — Stacked bars by investment category (Agency Debt, Treasury Debt, Repos, etc.)
2. **Maturity Buckets** — Stacked bars by WAL bucket (<=1d through 180+d)
3. **AUM Flow** — Line chart of AUM with MoM change bars (green/red)
4. **Liquidity Ratios** — Daily and weekly liquidity % with regulatory minimums
5. **HHI Concentration** — Herfindahl-Hirschman Index with concentration zone shading

### Top Issuers (`/mmf-issuers`)
Horizontal bar chart of top 10 issuers by % of NAV at the latest reporting date.

---

## Regulatory Thresholds

| Metric | Minimum |
|--------|---------|
| Daily liquid assets | 10% of NAV |
| Weekly liquid assets | 30% of NAV |
| HHI (competitive) | < 1,500 |
| HHI (moderate concentration) | 1,500–2,500 |
| HHI (high concentration) | > 2,500 |
