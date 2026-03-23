"""
BQL validation and query construction helpers.
"""

from __future__ import annotations

import re
from typing import Any


def validate_bql(query: str) -> dict[str, Any]:
    """Validate BQL query syntax and return issues found.

    Returns ``{"valid": bool, "issues": [str, ...]}``.
    """
    issues: list[str] = []
    query_lower = query.lower()

    # Required clauses
    if "get(" not in query_lower:
        issues.append("Missing required get() clause")
    if "for(" not in query_lower:
        issues.append("Missing required for() clause")

    # Ticker list bracket syntax
    for_match = re.search(r"for\s*\(\s*'([^']+)'\s*\)", query)
    if for_match:
        dynamic_funcs = ("members", "filter", "bondsuniv", "loansuniv", "segments", "intersect", "union")
        if not any(fn in query_lower for fn in dynamic_funcs):
            issues.append("Tickers must be in brackets: for(['ticker']) not for('ticker')")

    # let() semicolons
    let_match = re.search(r"let\s*\((.+?)\)\s*(?:get|$)", query, re.IGNORECASE | re.DOTALL)
    if let_match:
        content = let_match.group(1)
        var_count = content.count("#")
        semicolons = content.count(";")
        if var_count > 0 and semicolons < var_count:
            issues.append(
                f"let() has {var_count} variable(s) but only {semicolons} semicolon(s); "
                "each variable assignment must end with ;"
            )

    # Single = used for comparison (should be ==)
    single_equals = re.findall(r"(\w+)\s*=\s*'", query)
    param_keywords = {"dates", "currency", "per", "fill", "fpt", "fpo", "mode", "fpr", "pricing_source"}
    for field in single_equals:
        if field.lower() not in param_keywords:
            issues.append(f"Use == for comparison: {field}=='value' (not =)")

    # Balanced parentheses
    opens = query.count("(")
    closes = query.count(")")
    if opens != closes:
        issues.append(f"Unbalanced parentheses: {opens} opening vs {closes} closing")

    return {"valid": len(issues) == 0, "issues": issues}


# ---------------------------------------------------------------------------
# BQL template scaffolding
# ---------------------------------------------------------------------------

_TEMPLATES: dict[str, dict[str, Any]] = {
    "price_snapshot": {
        "description": "Current price for a list of securities",
        "template": "get({fields}) for([{tickers}])",
        "defaults": {"fields": "px_last", "tickers": "'SPY US Equity'"},
    },
    "historical_timeseries": {
        "description": "Historical time series with date range",
        "template": "get({fields}) for([{tickers}]) with(dates=range({start},{end}))",
        "defaults": {
            "fields": "px_last",
            "tickers": "'SPY US Equity'",
            "start": "-1Y",
            "end": "0D",
        },
    },
    "index_members": {
        "description": "Data for all members of an index",
        "template": "get({fields}) for(members(['{index}']))",
        "defaults": {"fields": "px_last, name", "index": "SPX Index"},
    },
    "bond_screening": {
        "description": "Screen active bonds by criteria",
        "template": (
            "get({fields}) for(filter(bondsUniv('active'), {filters}))"
        ),
        "defaults": {
            "fields": "name, yield(), spread()",
            "filters": "crncy=='USD' and rtg_sp() in ['A+','A','A-']",
        },
    },
    "sector_aggregation": {
        "description": "Aggregate metric by sector/group",
        "template": (
            "get(avg(group({metric}, {group_by}))) "
            "for(members(['{index}']))"
        ),
        "defaults": {
            "metric": "pe_ratio()",
            "group_by": "gics_sector_name()",
            "index": "SPX Index",
        },
    },
    "fundamentals": {
        "description": "Fundamental data with period overrides",
        "template": "get({fields}) for([{tickers}])",
        "defaults": {
            "fields": "is_eps(fpt=A, fpo=0), sales_rev_turn(fpt=A, fpo=0)",
            "tickers": "'IBM US Equity'",
        },
    },
}


def build_bql_from_intent(
    intent: str, universe_type: str | None = None
) -> dict[str, Any]:
    """Return matching BQL template scaffolding for a given intent description."""
    intent_lower = intent.lower()

    if any(kw in intent_lower for kw in ("screen", "filter", "bond")):
        key = "bond_screening"
    elif any(kw in intent_lower for kw in ("history", "historical", "timeseries", "time series")):
        key = "historical_timeseries"
    elif any(kw in intent_lower for kw in ("member", "index", "constituent")):
        key = "index_members"
    elif any(kw in intent_lower for kw in ("sector", "aggregate", "group", "average")):
        key = "sector_aggregation"
    elif any(kw in intent_lower for kw in ("fundamental", "earnings", "revenue", "eps")):
        key = "fundamentals"
    else:
        key = "price_snapshot"

    tpl = _TEMPLATES[key]

    return {
        "template_name": key,
        "description": tpl["description"],
        "template": tpl["template"],
        "defaults": tpl["defaults"],
        "rules": [
            "Tickers in for() must be wrapped in brackets: for(['TICKER'])",
            "Use == for comparisons (not =)",
            "Each let() variable must end with ;",
            "Ensure parentheses are balanced",
            "String values use single quotes: crncy=='USD'",
        ],
        "examples": [
            "get(px_last) for(['IBM US Equity'])",
            "get(px_last) for(members(['SPX Index'])) with(dates=range(-1Y,0D))",
            "get(name, yield(), spread()) for(filter(bondsUniv('active'), crncy=='USD'))",
        ],
    }
