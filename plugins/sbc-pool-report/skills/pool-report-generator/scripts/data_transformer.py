#!/usr/bin/env python3
"""
Data Transformer for SBC Pool Report

Converts raw SQL query results + FRED data into the JSON structure
expected by generate_pptx.js.

Usage:
    python3 data_transformer.py <holdings.json> <fred_data.json> <output.json>

Or import as a module:
    from data_transformer import transform_all
    result = transform_all(holdings_rows, fred_data, report_date)
"""

import json
import sys
from datetime import datetime, timedelta
from collections import defaultdict

# ─── Security Type Mapping ────────────────────────────────────────────────

SECURITY_TYPE_MAP = {
    ("USAGENCY", "CMO/REMIC", None): "Agency Mortgage-Backed",
    ("USAGENCY", "ABS", None): "Agency Mortgage-Backed",
    ("CORP", "CMO/REMIC", None): "Asset-Backed Securities",
    ("MM", "COMMPAPER", None): "Commercial Paper",
    ("CORP", "NOTESBONDS", None): "Corporate Notes",
    ("USAGENCY", "DISCNOTE", None): "Federal Agencies",
    ("USAGENCY", "NOTESBONDS", None): "Federal Agencies",
    ("USGOV", "NOTESBONDS", None): "U.S. Treasuries",
    ("OTHER", "NOTESBONDS", None): "Supranationals",
    ("MM", "CD", "401"): "Joint Powers Authority",
    ("MM", "CD", "410"): "Repurchase Agreements",
    ("MM", "CD", "415"): "Money Market Funds",
}

STABLE_NAV_TYPES = {"Money Market Funds", "Joint Powers Authority"}

IMPLIED_RATINGS = {
    "U.S. Treasuries": ("AA+", "Aa1"),
    "Federal Agencies": ("AA+", "Aa1"),
    "Agency Mortgage-Backed": ("AA+", "Aa1"),
}

# Policy limits from IPS Schedule I
POLICY_LIMITS = {
    "U.S. Treasuries": 100,
    "Federal Agencies": 100,
    "Agency Mortgage-Backed": 100,
    "Asset-Backed Securities": 20,
    "Commercial Paper": 25,
    "Corporate Notes": 30,
    "Joint Powers Authority": 15,
    "Money Market Funds": 20,
    "Repurchase Agreements": 40,
    "Supranationals": 30,
}

SP_RATING_ORDER = [
    "AAA", "AAAM", "AA+", "AA", "AA-", "A+", "A", "A-",
    "A-1+", "A-1", "BBB+", "BBB", "BBB-", "NR"
]

MOODYS_RATING_ORDER = [
    "Aaa", "Aa1", "Aa2", "Aa3", "A1", "A2", "A3",
    "Baa1", "Baa2", "Baa3", "P-1", "NR"
]

MATURITY_BUCKETS = [
    ("O/N", 0, 1),
    ("1-6 mo", 2, 180),
    ("6-12 mo", 181, 365),
    ("12-18 mo", 366, 545),
    ("18-24 mo", 546, 730),
    ("24-30 mo", 731, 912),
    ("30-36 mo", 913, 1095),
    ("36-42 mo", 1096, 1278),
    ("42-48 mo", 1279, 1460),
    ("48-54 mo", 1461, 1643),
    ("54-60 mo", 1644, 1825),
    ("Over 60 mo", 1826, 999999),
]


def classify_security(cat, subcat, sec_cd):
    """Map a holding to its standardized security type."""
    # Try specific match first (with sec_cd)
    key_specific = (cat, subcat, str(sec_cd).strip() if sec_cd else None)
    if key_specific in SECURITY_TYPE_MAP:
        return SECURITY_TYPE_MAP[key_specific]
    # Try generic match (without sec_cd)
    key_generic = (cat, subcat, None)
    if key_generic in SECURITY_TYPE_MAP:
        return SECURITY_TYPE_MAP[key_generic]
    return "Other"


def apply_nav_fix(holding, sec_type):
    """Apply stable NAV fix for MMF and JPA."""
    if sec_type in STABLE_NAV_TYPES:
        holding["Market_Val"] = holding["Par_Val"]
        holding["Book_Val"] = holding["Par_Val"]
    return holding


def apply_duration_filter(dura):
    """Filter invalid duration values."""
    if dura is None or dura > 100:
        return 0.0
    return float(dura)


def apply_implied_ratings(holding, sec_type):
    """Apply implied credit ratings for unrated securities."""
    sp = holding.get("SP", "").strip() if holding.get("SP") else ""
    mdy = holding.get("Mdy", "").strip() if holding.get("Mdy") else ""
    if (not sp or sp in ("", "NR", "N/A")) and sec_type in IMPLIED_RATINGS:
        holding["SP"] = IMPLIED_RATINGS[sec_type][0]
    if (not mdy or mdy in ("", "NR", "N/A")) and sec_type in IMPLIED_RATINGS:
        holding["Mdy"] = IMPLIED_RATINGS[sec_type][1]
    return holding


def parse_date_int(date_int, report_date_int):
    """Parse YYYYMMDD integer to datetime. Handle special values."""
    if date_int is None or date_int >= 99990000:
        return None
    try:
        return datetime.strptime(str(int(date_int)), "%Y%m%d")
    except (ValueError, TypeError):
        return None


def assign_maturity_bucket(holding, sec_type, report_date):
    """Assign a holding to its maturity bucket."""
    if sec_type in STABLE_NAV_TYPES:
        return "O/N"
    mat_dt = holding.get("Mat_dt")
    maturity = parse_date_int(mat_dt, None)
    if maturity is None:
        return "O/N"
    days = (maturity - report_date).days
    if days <= 1:
        return "O/N"
    for label, lo, hi in MATURITY_BUCKETS:
        if lo <= days <= hi:
            return label
    return "Over 60 mo"


def format_currency(value, abbreviate=True):
    """Format a dollar amount."""
    if abbreviate:
        if abs(value) >= 1e9:
            return f"${value / 1e9:,.2f}B"
        elif abs(value) >= 1e6:
            return f"${value / 1e6:,.1f}M"
        else:
            return f"${value:,.0f}"
    return f"${value:,.2f}"


def transform_holdings(holdings, report_date_int):
    """Transform raw holdings into classified, fixed records."""
    report_date = datetime.strptime(str(report_date_int), "%Y%m%d")
    transformed = []

    for h in holdings:
        sec_type = classify_security(
            h.get("Cat_Desc", ""),
            h.get("SubCat_Desc", ""),
            h.get("Sec_Cd")
        )
        h = apply_nav_fix(h, sec_type)
        h = apply_implied_ratings(h, sec_type)
        h["Dura"] = apply_duration_filter(h.get("Dura"))
        h["Book_Yld"] = float(h.get("Book_Yld", 0) or 0)
        h["security_type"] = sec_type
        h["maturity_bucket"] = assign_maturity_bucket(h, sec_type, report_date)
        transformed.append(h)

    return transformed


def aggregate_portfolio(holdings):
    """Calculate portfolio-level aggregates."""
    total_mv = sum(h["Market_Val"] for h in holdings)
    total_pv = sum(h["Par_Val"] for h in holdings)
    total_bv = sum(h.get("Book_Val", 0) for h in holdings)

    # Weighted averages (market-value-weighted)
    wa_yield = sum(h["Book_Yld"] * h["Market_Val"] for h in holdings) / total_mv if total_mv else 0
    wa_duration = sum(h["Dura"] * h["Market_Val"] for h in holdings) / total_mv if total_mv else 0

    return {
        "total_market_value": total_mv,
        "total_par_value": total_pv,
        "total_book_value": total_bv,
        "unrealized_gain_loss": total_mv - total_bv,
        "market_to_book_ratio": total_mv / total_bv if total_bv else 0,
        "weighted_avg_yield": wa_yield,
        "weighted_avg_duration": wa_duration,
        "num_holdings": len(holdings),
        "num_sectors": len(set(h["security_type"] for h in holdings)),
    }


def aggregate_sectors(holdings, total_mv):
    """Sector allocation breakdown."""
    sectors = defaultdict(lambda: {"mv": 0, "pv": 0, "bv": 0, "count": 0, "yields": [], "durations": []})
    for h in holdings:
        s = sectors[h["security_type"]]
        s["mv"] += h["Market_Val"]
        s["pv"] += h["Par_Val"]
        s["bv"] += h.get("Book_Val", 0)
        s["count"] += 1
        s["yields"].append(h["Book_Yld"])
        s["durations"].append(h["Dura"])

    result = []
    for name, s in sorted(sectors.items(), key=lambda x: -x[1]["mv"]):
        pct = (s["mv"] / total_mv * 100) if total_mv else 0
        avg_yield = sum(s["yields"]) / len(s["yields"]) if s["yields"] else 0
        avg_dur = sum(s["durations"]) / len(s["durations"]) if s["durations"] else 0
        result.append({
            "name": name,
            "market_value": s["mv"],
            "par_value": s["pv"],
            "pct_portfolio": round(pct, 1),
            "avg_yield": round(avg_yield, 2),
            "avg_duration": round(avg_dur, 2),
            "count": s["count"],
        })
    return result


def aggregate_credit_quality(holdings, total_mv):
    """Credit quality distribution for S&P and Moody's."""
    sp_dist = defaultdict(float)
    mdy_dist = defaultdict(float)
    for h in holdings:
        sp = (h.get("SP") or "NR").strip()
        mdy = (h.get("Mdy") or "NR").strip()
        sp_dist[sp] += h["Market_Val"]
        mdy_dist[mdy] += h["Market_Val"]

    def to_list(dist, order):
        result = []
        for rating in order:
            if rating in dist:
                pct = round(dist[rating] / total_mv * 100, 1)
                result.append({"rating": rating, "pct": pct})
        # Add any ratings not in order
        for rating, mv in dist.items():
            if rating not in order:
                pct = round(mv / total_mv * 100, 1)
                result.append({"rating": rating, "pct": pct})
        return result

    return {
        "sp": to_list(sp_dist, SP_RATING_ORDER),
        "moodys": to_list(mdy_dist, MOODYS_RATING_ORDER),
    }


def aggregate_maturity(holdings, total_mv):
    """Maturity distribution by bucket and security type."""
    buckets = defaultdict(lambda: defaultdict(float))
    for h in holdings:
        buckets[h["maturity_bucket"]][h["security_type"]] += h["Market_Val"]

    result = []
    for label, _, _ in MATURITY_BUCKETS:
        if label in buckets:
            total = sum(buckets[label].values())
            result.append({
                "bucket": label,
                "total": total,
                "pct": round(total / total_mv * 100, 1) if total_mv else 0,
                "by_type": dict(buckets[label]),
            })
    return result


def check_compliance(sectors):
    """Check Investment Policy compliance for each sector."""
    results = []
    for s in sectors:
        name = s["name"]
        actual = s["pct_portfolio"]
        limit = POLICY_LIMITS.get(name, 100)
        margin = round(limit - actual, 1)

        if actual > limit:
            status = "EXCEEDS"
        elif actual > limit * 0.9:
            status = "Near Limit"
        else:
            status = "COMPLIANT"

        results.append({
            "security_type": name,
            "actual_pct": actual,
            "policy_limit": limit,
            "margin": margin,
            "status": status,
        })
    return results


def _classify_parent_issuer(long_desc):
    """Map a holding's Long_Desc_1 to its parent issuer name.

    Uses pattern matching on the security description to consolidate
    holdings under their parent entity (e.g., all FHLMC REMICs, FRESB,
    and Gold pools map to 'FHLMC (Freddie Mac)').
    """
    desc = (long_desc or "").upper().strip()

    # Freddie Mac family: REMICs, FRESB, multifamily, Gold PCs
    if any(k in desc for k in ("FHLMC", "FREDDIE", "FRESB")):
        return "FHLMC (Freddie Mac)"

    # Federal Home Loan Banks
    if "FHLB" in desc or "FED HOME LN" in desc:
        return "FHLB (Federal Home Loan Banks)"

    # U.S. Treasury
    if any(k in desc for k in ("US TREASURY", "U.S. TREASURY", "UNITED STATES TREAS",
                                 "T-NOTE", "T-BILL", "T-BOND", "UST ")):
        return "U.S. Treasury"

    # Fidelity (money market)
    if "FIDELITY" in desc:
        return "Fidelity Investments"

    # Toyota Motor Credit (auto ABS trusts)
    if any(k in desc for k in ("TOYOTA", "TOYO")):
        return "Toyota Motor Credit"

    # MetLife
    if "METLIFE" in desc or "MET LIFE" in desc:
        return "MetLife"

    # Fannie Mae
    if any(k in desc for k in ("FNMA", "FANNIE", "FAN MAE")):
        return "FNMA (Fannie Mae)"

    # California JPA pools
    if any(k in desc for k in ("CAMP", "CALTRUST", "CAL TRUST", "JPA",
                                 "CALIFORNIA ASSET")):
        return "California JPA (CAMP/CalTRUST)"

    # JPMorgan Chase
    if any(k in desc for k in ("JPMORGAN", "JP MORGAN", "CHASE")):
        return "JPMorgan Chase"

    # Federal Farm Credit Banks
    if any(k in desc for k in ("FARM CREDIT", "FFCB", "FED FARM")):
        return "Federal Farm Credit Banks"

    # Bank of America
    if any(k in desc for k in ("BANK OF AMER", "BOA ", "BOFA")):
        return "Bank of America"

    # Goldman Sachs
    if "GOLDMAN" in desc:
        return "Goldman Sachs"

    # Morgan Stanley
    if "MORGAN STANLEY" in desc:
        return "Morgan Stanley"

    # John Deere (ABS trusts)
    if any(k in desc for k in ("JOHN DEERE", "DEERE")):
        return "John Deere"

    # Honda (auto ABS)
    if "HONDA" in desc:
        return "Honda"

    # Hyundai (auto ABS)
    if "HYUNDAI" in desc:
        return "Hyundai"

    # International Bank for Reconstruction (World Bank)
    if any(k in desc for k in ("INTL BK RECON", "WORLD BANK", "IBRD")):
        return "World Bank (IBRD)"

    # Inter-American Development Bank
    if any(k in desc for k in ("INTER-AMER", "IADB")):
        return "Inter-American Dev Bank"

    # Supranationals catch-all
    if any(k in desc for k in ("SUPRA", "AFRICAN DEV", "ASIAN DEV")):
        return desc[:30].title()

    # Fallback: use first 3 words of description
    parts = desc.split()
    return " ".join(parts[:3]).title() if len(parts) >= 3 else desc.title()


def aggregate_issuer_concentration(holdings, total_mv, top_n=10):
    """Top issuers by market value with parent-issuer consolidation."""
    issuers = defaultdict(lambda: {"mv": 0, "count": 0})
    for h in holdings:
        # Use Long_Desc_1 for parent-issuer classification
        desc = h.get("Long_Desc_1") or h.get("Short_Desc") or "Unknown"
        parent = _classify_parent_issuer(desc)
        issuers[parent]["mv"] += h["Market_Val"]
        issuers[parent]["count"] += 1

    sorted_issuers = sorted(issuers.items(), key=lambda x: -x[1]["mv"])[:top_n]
    return [
        {
            "issuer": name,
            "market_value": data["mv"],
            "pct": round(data["mv"] / total_mv * 100, 1) if total_mv else 0,
            "count": data["count"],
        }
        for name, data in sorted_issuers
    ]


def calculate_monthly_income(sectors):
    """Estimate monthly coupon income by sector."""
    result = []
    total = 0
    for s in sectors:
        monthly = s["market_value"] * (s["avg_yield"] / 100) / 12
        total += monthly
        result.append({
            "sector": s["name"],
            "yield": s["avg_yield"],
            "monthly_income": monthly,
        })
    return result, total


def calculate_horizon_analysis(wa_yield, wa_duration):
    """Simple horizon analysis under parallel rate shift scenarios."""
    scenarios = [-100, -50, 0, 50, 100]
    results = []
    for shift in scenarios:
        income_return = wa_yield
        price_return = -wa_duration * (shift / 100)
        total_return = income_return + price_return
        results.append({
            "scenario": f"{'+' if shift > 0 else ''}{shift} bps",
            "shift_bps": shift,
            "income": round(income_return, 2),
            "price": round(price_return, 2),
            "total": round(total_return, 2),
        })
    return results


# ─── Economic Data Transformation (Phase 2A — NEW in v2) ────────────────

def transform_economic_data(fred_data):
    """
    Transform raw FRED data into economic metrics for charts and commentary.

    Args:
        fred_data: dict with 'latest' and 'history' keys from Phase 1B

    Returns:
        dict with calculated economic metrics and chart-ready series
    """
    economic = {}

    latest = fred_data.get("latest", {})
    history = fred_data.get("history", {})

    # --- Fed Funds Rate ---
    fed_latest = latest.get("FEDFUNDS", {})
    economic["fed_rate"] = fed_latest.get("value", 0)
    fed_hist = history.get("FEDFUNDS", {}).get("observations", [])
    economic["fed_rate_history"] = [
        {"date": obs["date"], "value": float(obs["value"])}
        for obs in fed_hist if obs.get("value") not in (None, ".", "")
    ]
    # Determine direction
    if len(economic["fed_rate_history"]) >= 2:
        prev = economic["fed_rate_history"][-2]["value"]
        curr = economic["fed_rate"]
        if curr > prev:
            economic["fed_rate_direction"] = "rising"
        elif curr < prev:
            economic["fed_rate_direction"] = "falling"
        else:
            economic["fed_rate_direction"] = "holding"
    else:
        economic["fed_rate_direction"] = "holding"

    # --- CPI Year-over-Year ---
    cpi_hist = history.get("CPIAUCSL", {}).get("observations", [])
    cpi_clean = [
        {"date": obs["date"], "value": float(obs["value"])}
        for obs in cpi_hist if obs.get("value") not in (None, ".", "")
    ]
    economic["cpi_yoy_history"] = []
    if len(cpi_clean) >= 13:
        # Calculate YoY % change for each month that has a 12-month-ago pair
        for i in range(12, len(cpi_clean)):
            current_val = cpi_clean[i]["value"]
            prior_val = cpi_clean[i - 12]["value"]
            if prior_val > 0:
                yoy = (current_val / prior_val - 1) * 100
                economic["cpi_yoy_history"].append({
                    "date": cpi_clean[i]["date"],
                    "value": round(yoy, 2)
                })
    if economic["cpi_yoy_history"]:
        economic["cpi_yoy"] = economic["cpi_yoy_history"][-1]["value"]
    else:
        # Fallback: calculate from latest 2 CPI values if available
        cpi_latest = latest.get("CPIAUCSL", {}).get("value")
        economic["cpi_yoy"] = None  # Will need web research fallback

    # --- Unemployment Rate ---
    economic["unemployment"] = latest.get("UNRATE", {}).get("value", 0)
    unemp_hist = history.get("UNRATE", {}).get("observations", [])
    economic["unemployment_history"] = [
        {"date": obs["date"], "value": float(obs["value"])}
        for obs in unemp_hist if obs.get("value") not in (None, ".", "")
    ]

    # --- AA Credit Spread ---
    # Use AA OAS (BAMLC0A2CAA) as primary; fall back to BBB if unavailable
    aa_spread_key = "BAMLC0A2CAA"
    if aa_spread_key not in latest:
        aa_spread_key = "BAMLC0A4CBBB"  # fallback
    economic["aa_spread"] = latest.get(aa_spread_key, {}).get("value", 0)
    aa_hist = history.get(aa_spread_key, {}).get("observations", [])
    economic["aa_spread_history"] = [
        {"date": obs["date"], "value": float(obs["value"])}
        for obs in aa_hist if obs.get("value") not in (None, ".", "")
    ]
    # Keep legacy key for backward compatibility
    economic["bbb_spread"] = economic["aa_spread"]
    economic["bbb_spread_history"] = economic["aa_spread_history"]
    # Spread change from prior month
    if len(economic["aa_spread_history"]) >= 2:
        economic["spread_change"] = round(
            economic["aa_spread_history"][-1]["value"] -
            economic["aa_spread_history"][-2]["value"], 2
        )
    else:
        economic["spread_change"] = 0

    # --- Yield Curve ---
    yield_curve = fred_data.get("yield_curve", {})
    economic["yield_curve_current"] = yield_curve.get("current", {})
    economic["yield_curve_prior"] = yield_curve.get("prior_year", {})

    # Curve slope
    dgs10 = latest.get("DGS10", {}).get("value", 0)
    dgs2 = latest.get("DGS2", {}).get("value", 0)
    t10y2y = latest.get("T10Y2Y", {}).get("value")
    economic["curve_slope"] = t10y2y if t10y2y is not None else (dgs10 - dgs2 if dgs10 and dgs2 else 0)

    # --- Real Return ---
    # Will be calculated in the report builder when portfolio yield is known

    # --- 10-Year Treasury ---
    economic["dgs10"] = dgs10

    # --- Mortgage rate (context) ---
    economic["mortgage_30y"] = latest.get("MORTGAGE30US", {}).get("value", 0)

    return economic


def prepare_economic_chart_data(economic):
    """
    Format economic data into chart-ready structures for chart_renderer.py.

    Args:
        economic: dict from transform_economic_data()

    Returns:
        dict with chart-ready data for each economic chart
    """
    charts = {}

    # Fed Funds Rate History chart data
    fed_hist = economic.get("fed_rate_history", [])
    if fed_hist:
        charts["fed_funds"] = {
            "labels": [_format_month_label(h["date"]) for h in fed_hist],
            "values": [h["value"] for h in fed_hist],
            "title": "Federal Funds Rate",
            "y_label": "Rate (%)",
        }

    # CPI YoY chart data
    cpi_hist = economic.get("cpi_yoy_history", [])
    if cpi_hist:
        charts["cpi_yoy"] = {
            "labels": [_format_month_label(h["date"]) for h in cpi_hist],
            "values": [h["value"] for h in cpi_hist],
            "title": "CPI Inflation (Year-over-Year)",
            "y_label": "Year-over-Year Change (%)",
            "reference_line": {"value": 2.0, "label": "Fed Target: 2%"},
        }

    # Unemployment chart data
    unemp_hist = economic.get("unemployment_history", [])
    if unemp_hist:
        charts["unemployment"] = {
            "labels": [_format_month_label(h["date"]) for h in unemp_hist],
            "values": [h["value"] for h in unemp_hist],
            "title": "Unemployment Rate",
            "y_label": "Rate (%)",
        }

    # AA Credit Spread chart data
    aa_hist = economic.get("aa_spread_history", [])
    if aa_hist:
        charts["aa_spread"] = {
            "labels": [_format_month_label(h["date"]) for h in aa_hist],
            "values": [h["value"] for h in aa_hist],
            "title": "AA Corporate Credit Spread",
            "y_label": "Spread (percentage points)",
        }
    # Keep legacy key for backward compat
    if "aa_spread" in charts:
        charts["bbb_spread"] = charts["aa_spread"]

    # Yield Curve Comparison chart data
    yc_current = economic.get("yield_curve_current", {})
    yc_prior = economic.get("yield_curve_prior", {})
    tenors = ["3M", "6M", "1Y", "2Y", "5Y", "10Y", "30Y"]
    if yc_current and yc_prior:
        current_vals = [yc_current.get(t, 0) for t in tenors]
        prior_vals = [yc_prior.get(t, 0) for t in tenors]
        charts["yield_curve_comparison"] = {
            "labels": tenors,
            "current": current_vals,
            "prior": prior_vals,
            "title": "Treasury Yield Curve",
        }

    return charts


def _format_month_label(date_str):
    """Convert '2025-03-01' to 'Mar' or '2025-03' to 'Mar'."""
    try:
        parts = date_str.split("-")
        months = ['Jan','Feb','Mar','Apr','May','Jun',
                  'Jul','Aug','Sep','Oct','Nov','Dec']
        m = int(parts[1]) - 1
        return months[m]
    except (ValueError, IndexError):
        return date_str[:7]


# ─── Updated Main Entry Point ───────────────────────────────────────────

def transform_all(holdings_rows, fred_data, report_date_int):
    """
    Main entry point. Transform raw data into the JSON structure for generate_pptx.js.

    Args:
        holdings_rows: list of dicts from SQL query
        fred_data: dict of FRED series data (latest + history)
        report_date_int: YYYYMMDD integer

    Returns:
        dict ready to serialize to JSON
    """
    # Parse report date
    report_date = datetime.strptime(str(report_date_int), "%Y%m%d")
    date_formatted = report_date.strftime("%B %d, %Y")

    # Transform holdings
    holdings = transform_holdings(holdings_rows, report_date_int)

    # Aggregates
    portfolio = aggregate_portfolio(holdings)
    total_mv = portfolio["total_market_value"]
    sectors = aggregate_sectors(holdings, total_mv)
    credit = aggregate_credit_quality(holdings, total_mv)
    maturity = aggregate_maturity(holdings, total_mv)
    compliance = check_compliance(sectors)
    issuers = aggregate_issuer_concentration(holdings, total_mv)
    income, total_income = calculate_monthly_income(sectors)
    horizon = calculate_horizon_analysis(
        portfolio["weighted_avg_yield"],
        portfolio["weighted_avg_duration"]
    )

    # Economic data transformation (v2)
    economic = {}
    economic_chart_data = {}
    if fred_data and fred_data.get("history"):
        economic = transform_economic_data(fred_data)
        economic_chart_data = prepare_economic_chart_data(economic)
        # Calculate real return now that we have portfolio yield
        if economic.get("cpi_yoy") is not None:
            economic["real_return"] = round(
                portfolio["weighted_avg_yield"] - economic["cpi_yoy"], 2
            )

    return {
        "report_date": date_formatted,
        "report_date_int": report_date_int,
        "portfolio": portfolio,
        "sectors": sectors,
        "credit_quality": credit,
        "maturity_distribution": maturity,
        "compliance": compliance,
        "issuer_concentration": issuers,
        "monthly_income": income,
        "total_monthly_income": total_income,
        "horizon_analysis": horizon,
        "fred_data": fred_data or {},
        "economic": economic,
        "economic_chart_data": economic_chart_data,
        "charts": {},  # Populated after chart generation
    }


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 data_transformer.py <holdings.json> <fred_data.json> <output.json>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        holdings = json.load(f)
    with open(sys.argv[2]) as f:
        fred = json.load(f)

    # Determine report date from first holding or use provided
    report_date = holdings[0].get("Rpt_Date", 20260130) if holdings else 20260130
    result = transform_all(holdings, fred, report_date)

    with open(sys.argv[3], "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"Transformed {len(holdings)} holdings -> {sys.argv[3]}")
    print(f"  Market Value: {format_currency(result['portfolio']['total_market_value'])}")
    print(f"  Sectors: {result['portfolio']['num_sectors']}")
    print(f"  Holdings: {result['portfolio']['num_holdings']}")
    if result.get("economic"):
        eco = result["economic"]
        print(f"  Fed Rate: {eco.get('fed_rate', 'N/A')}%")
        print(f"  CPI YoY: {eco.get('cpi_yoy', 'N/A')}%")
        print(f"  Unemployment: {eco.get('unemployment', 'N/A')}%")
        print(f"  AA Spread: {eco.get('aa_spread', 'N/A')}%")
        print(f"  Curve Slope: {eco.get('curve_slope', 'N/A')}%")
