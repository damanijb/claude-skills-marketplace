# Database Data Dictionary

## Connection
- **Server:** treasurer.database.windows.net
- **Database:** ATC_TREASURER
- **Schema:** portfolio
- **Access:** Use the `azure-sql-treasurer` skill

## Core Tables

### portfolio.fis_gold_extract (Primary for Reports)
Position-level data from FIS Gold system. ~360 holdings per report date.

| Column | Type | Notes |
|--------|------|-------|
| id | int | PK |
| Rpt_Date | int | YYYYMMDD format (e.g., 20251231) |
| Cusip | varchar(20) | Security CUSIP |
| Short_Desc | varchar(100) | Security description |
| Cat_Desc | varchar(50) | Category: USGOV, USAGENCY, CORP, MM, OTHER |
| SubCat_Desc | varchar(50) | Subcategory: NOTESBONDS, CMO/REMIC, ABS, CD, COMMPAPER, DISCNOTE |
| Sec_Cd | varchar(20) | Security code (401=JPA, 410=Repo, 415=MMF) |
| [Group] | varchar(50) | FIS group classification |
| Par_Val | decimal | Par/face value |
| Book_Val | decimal | Book/amortized cost |
| Market_Val | decimal | Current market value |
| Rate | decimal | Coupon rate (%) |
| Book_Yld | decimal | Book yield (%) |
| Dura | decimal | Modified duration (years). 999.99 = N/A |
| Mat_dt | int | Maturity date YYYYMMDD. 99990101 = perpetual |
| SP | varchar(20) | S&P rating |
| Mdy | varchar(20) | Moody's rating |
| Accru_Todate | decimal | Accrued interest to date |
| Mtd_Accru | decimal | Month-to-date accrual |
| WAC | decimal | Weighted average coupon |
| WAL | decimal | Weighted average life |
| WAM | int | Weighted average maturity (months) |
| CPR | decimal | Conditional prepayment rate |
| Intent | varchar(20) | AFS or HTM |
| Nxt_Int_Dt | int | Next interest date |
| Nxt_Int_Amt | decimal | Next interest amount |

### portfolio.pfm (Alternative Position Table)
Standardized portfolio positions with cleaner field names.

| Column | Type | Notes |
|--------|------|-------|
| date | date | Position date |
| cusip | varchar(9) | CUSIP |
| description | varchar | Full description |
| security_type | varchar(50) | Type classification |
| issuer | varchar | Issuer name |
| sector | varchar(50) | Sector |
| quantity | float | Holdings quantity |
| par_value | float | Par value |
| market_value | float | Market value |
| original_cost | float | Cost basis |
| price | float | Current price |
| yield | float | Yield |
| duration | float | Duration |
| maturity_date | date | Maturity |
| settlement_date | date | Settlement |
| sp_rating | varchar(50) | S&P rating |
| fitch_rating | varchar(50) | Fitch rating |

### portfolio.cashflow
Cash position forecasting data.

| Column | Type | Notes |
|--------|------|-------|
| Date | datetime | Cash flow date |
| InvMaturing | float | Investments maturing |
| MoneyIn | float | Cash inflows |
| TotalRev | float | Total revenues |
| InvPurchased | float | Investments purchased |
| Disbursements | float | Disbursements |
| ProjInvPoolBal | float | Projected pool balance |
| ActPoolBal | float | Actual pool balance |

### portfolio.latest_pfm (VIEW)
Most recent snapshot from pfm table. Same columns as pfm.

### portfolio.sympro
Historical transaction data (543K+ records). Use for trade analysis.

## Available Report Dates
Query to find available dates:
```sql
SELECT DISTINCT Rpt_Date FROM portfolio.fis_gold_extract ORDER BY Rpt_Date DESC
```

Current dates: 20260130, 20251231, 20251103

## Key Queries

### Full Holdings Extract
```sql
SELECT
    Cat_Desc, SubCat_Desc, Sec_Cd,
    CAST(Par_Val AS FLOAT) AS Par_Val,
    CAST(Book_Val AS FLOAT) AS Book_Val,
    CAST(Market_Val AS FLOAT) AS Market_Val,
    CAST(Book_Yld AS FLOAT) AS Book_Yld,
    CAST(Dura AS FLOAT) AS Dura,
    CAST(Rate AS FLOAT) AS Rate,
    Mat_dt, SP, Mdy,
    CAST(Accru_Todate AS FLOAT) AS Accru_Todate,
    Cusip, Short_Desc, [Group]
FROM portfolio.fis_gold_extract
WHERE Rpt_Date = {report_date_int}
ORDER BY Market_Val DESC
```

### Sector Summary
```sql
SELECT
    security_type, COUNT(*) AS positions,
    SUM(CAST(market_value AS FLOAT)) AS total_mv,
    AVG(CAST(yield AS FLOAT)) AS avg_yield,
    AVG(CAST(duration AS FLOAT)) AS avg_duration
FROM portfolio.latest_pfm
GROUP BY security_type
ORDER BY total_mv DESC
```

### Credit Distribution
```sql
SELECT
    COALESCE(sp_rating, 'NR') AS rating,
    COUNT(*) AS count,
    SUM(CAST(market_value AS FLOAT)) AS total_value
FROM portfolio.latest_pfm
GROUP BY sp_rating
ORDER BY total_value DESC
```

### Upcoming Maturities
```sql
SELECT cusip, description, maturity_date, market_value, security_type,
    DATEDIFF(day, GETDATE(), maturity_date) AS days_to_maturity
FROM portfolio.latest_pfm
WHERE maturity_date <= DATEADD(day, 90, GETDATE())
ORDER BY maturity_date
```

---

## FRED Economic Data

### Series for Latest Values
Pull current readings using `fred_get_latest_value`:

| Series ID | Description | Units | Frequency |
|-----------|------------|-------|-----------|
| FEDFUNDS | Federal Funds Effective Rate | % | Monthly |
| SOFR | Secured Overnight Financing Rate | % | Daily |
| DTB3 | 3-Month Treasury Bill | % | Daily |
| DTB6 | 6-Month Treasury Bill | % | Daily |
| DGS1 | 1-Year Treasury Constant Maturity | % | Daily |
| DGS2 | 2-Year Treasury Constant Maturity | % | Daily |
| DGS5 | 5-Year Treasury Constant Maturity | % | Daily |
| DGS10 | 10-Year Treasury Constant Maturity | % | Daily |
| DGS30 | 30-Year Treasury Constant Maturity | % | Daily |
| CPIAUCSL | Consumer Price Index (All Urban) | Index 1982-84=100 | Monthly |
| UNRATE | Unemployment Rate | % | Monthly |
| BAMLC0A4CBBB | ICE BofA BBB US Corporate OAS | % | Daily |
| T10Y2Y | 10-Year minus 2-Year Treasury Spread | % | Daily |
| MORTGAGE30US | 30-Year Fixed Mortgage Rate | % | Weekly |

### Series for 12-Month History (Trend Charts)
Pull using `fred_get_series` with `observation_start` = 12 months ago:

| Series ID | Chart Use | Calculation |
|-----------|----------|-------------|
| FEDFUNDS | Fed Funds Rate History (line + area) | Direct value |
| CPIAUCSL | CPI Year-over-Year (line) | YoY % change: `(current / value_12mo_ago - 1) * 100` |
| UNRATE | Unemployment Rate (line) | Direct value |
| BAMLC0A4CBBB | BBB Credit Spread (line + area) | Direct value |
| DGS3MO, DGS6MO, DGS1, DGS2, DGS5, DGS10, DGS30 | Yield Curve Comparison | Current vs 12-month-ago values |

### Additional Series (GDP, PCE)
| Series ID | Description | Units | Frequency |
|-----------|------------|-------|-----------|
| PCEPI | PCE Price Index | Index 2017=100 | Monthly |
| A191RL1Q225SBEA | Real GDP Growth Rate | % Change (annualized) | Quarterly |

### Calculated Fields

```python
# CPI Year-over-Year percentage change
cpi_yoy = (cpi_current / cpi_12_months_ago - 1) * 100

# Fed Funds rate change direction
if current_rate > prior_month_rate:
    direction = "rising"
elif current_rate < prior_month_rate:
    direction = "falling"
else:
    direction = "holding"

# Yield curve slope
curve_slope = dgs10 - dgs2  # positive = normal, negative = inverted

# Real return
real_return = portfolio_yield - cpi_yoy

# Credit spread change
spread_change = current_bbb_oas - prior_month_bbb_oas
```

---

## Output Schemas

### FRED Data Output (`/tmp/sbc_fred_data.json`)
```json
{
  "pull_date": "2026-02-12",
  "latest": {
    "FEDFUNDS": {"value": 4.33, "date": "2026-01-01"},
    "SOFR": {"value": 4.31, "date": "2026-02-10"},
    "DTB3": {"value": 4.25, "date": "2026-02-10"},
    "DGS10": {"value": 4.50, "date": "2026-02-10"},
    "CPIAUCSL": {"value": 315.6, "date": "2026-01-01"},
    "UNRATE": {"value": 4.3, "date": "2026-01-01"},
    "BAMLC0A4CBBB": {"value": 1.15, "date": "2026-02-10"},
    "T10Y2Y": {"value": 0.25, "date": "2026-02-10"}
  },
  "history": {
    "FEDFUNDS": {
      "series_id": "FEDFUNDS",
      "observations": [
        {"date": "2025-02-01", "value": 4.33},
        {"date": "2025-03-01", "value": 4.33}
      ]
    },
    "CPIAUCSL": {
      "series_id": "CPIAUCSL",
      "observations": [
        {"date": "2025-02-01", "value": 308.2},
        {"date": "2025-03-01", "value": 309.1}
      ]
    }
  },
  "yield_curve": {
    "current": {
      "3M": 4.25, "6M": 4.30, "1Y": 4.28,
      "2Y": 4.15, "5Y": 4.20, "10Y": 4.50, "30Y": 4.70
    },
    "prior_year": {
      "3M": 5.20, "6M": 5.15, "1Y": 4.90,
      "2Y": 4.60, "5Y": 4.30, "10Y": 4.40, "30Y": 4.55
    }
  }
}
```

### Economic Research Output (`/tmp/sbc_economic_research.json`)
```json
{
  "research_date": "February 12, 2026",
  "fed_policy": {
    "headline": "Fed holds rates at 4.25-4.50% range",
    "detail": "The FOMC voted unanimously to maintain...",
    "forward_guidance": "Dot plot suggests 2 more cuts in 2026...",
    "data_points": {
      "current_rate": 4.33,
      "last_change": "December 2025",
      "direction": "holding"
    }
  },
  "inflation": {
    "headline": "CPI inflation at 2.8%, trending toward target",
    "detail": "...",
    "data_points": {"cpi_yoy": 2.8, "pce_yoy": 2.5, "core_cpi": 3.1}
  },
  "employment": {
    "headline": "Unemployment steady at 4.3%",
    "detail": "...",
    "data_points": {"unemployment": 4.3, "nonfarm_payrolls": 150000}
  },
  "credit_markets": {
    "headline": "IG spreads tight at 115 bps",
    "detail": "...",
    "data_points": {"ig_spread": 1.15, "hy_spread": 3.2}
  },
  "market_themes": [
    {
      "title": "Fed Rate Cut Expectations",
      "narrative": "Markets now expect...",
      "chart_suggestion": "FEDFUNDS history",
      "relevance": "HIGH"
    }
  ]
}
```

### Economic Commentary Output (`/tmp/sbc_economic_commentary.json`)
```json
{
  "slides": {
    "economic_overview": {
      "headline": "Economy Growing at Moderate Pace",
      "narrative": "The U.S. economy continues to expand...",
      "portfolio_impact": "Current conditions support...",
      "kpi_cards": [
        {"label": "Fed Funds Rate", "value": "4.33%", "source": "FEDFUNDS"},
        {"label": "Unemployment", "value": "4.3%", "source": "UNRATE"},
        {"label": "Inflation (CPI YoY)", "value": "2.8%", "source": "calculated"},
        {"label": "10-Year Treasury", "value": "4.50%", "source": "DGS10"},
        {"label": "IG Credit Spread", "value": "115 bps", "source": "BAMLC0A4CBBB"},
        {"label": "10Y-2Y Spread", "value": "0.25%", "source": "T10Y2Y"}
      ]
    },
    "fed_rates": {
      "headline": "The Fed held rates steady at 4.33%",
      "narrative": "When the Fed holds rates...",
      "portfolio_impact": "Short-term holdings continue earning..."
    },
    "inflation": {
      "headline": "Inflation fell to 2.8%, approaching the Fed's 2% target",
      "narrative": "...",
      "portfolio_impact": "Real return calculation..."
    },
    "labor_market": {
      "headline": "Unemployment held steady at 4.3%",
      "narrative": "...",
      "portfolio_impact": "..."
    },
    "yield_curve": {
      "headline": "The yield curve is positively sloped...",
      "narrative": "...",
      "portfolio_impact": "..."
    },
    "credit_markets": {
      "headline": "Investment-grade credit spreads at 115 bps",
      "narrative": "...",
      "portfolio_impact": "..."
    },
    "theme_1": {
      "section_label": "MARKET THEME",
      "headline": "...",
      "narrative": "...",
      "significance": "HIGH",
      "portfolio_impact": "..."
    },
    "theme_2": {
      "section_label": "MARKET THEME",
      "headline": "...",
      "narrative": "...",
      "significance": "MODERATE",
      "portfolio_impact": "..."
    },
    "economic_summary": {
      "key_takeaways": ["...", "...", "...", "..."],
      "portfolio_implications": "Given these economic conditions..."
    }
  }
}
```

### Report Data Output (`/tmp/sbc_report_data.json`)
Same as existing `report_data.json` structure, with these additions:

```json
{
  "economic": {
    "cpi_yoy": 2.8,
    "cpi_yoy_history": [{"date": "2025-02", "value": 2.9}, ...],
    "fed_rate": 4.33,
    "fed_rate_history": [{"date": "2025-02", "value": 4.33}, ...],
    "unemployment": 4.3,
    "unemployment_history": [{"date": "2025-02", "value": 4.1}, ...],
    "bbb_spread": 1.15,
    "bbb_spread_history": [{"date": "2025-02", "value": 1.20}, ...],
    "real_return": 0.8,
    "curve_slope": 0.25,
    "yield_curve_current": {"3M": 4.25, "6M": 4.30, ...},
    "yield_curve_prior": {"3M": 5.20, "6M": 5.15, ...}
  }
}
```
