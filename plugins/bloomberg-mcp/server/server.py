"""
Bloomberg MCP Server — FastMCP implementation.

Exposes 9 tools for Bloomberg data access, BQL queries, screening,
and field search.  Designed for Claude Code integration.

Run via: python run_server.py
"""

from __future__ import annotations

import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator

# Ensure local modules are importable
sys.path.insert(0, str(Path(__file__).parent))

from fastmcp import FastMCP, Context

from bloomberg_client import BloombergClient
from bql_builder import build_bql_from_intent, validate_bql
from utils import check_bloomberg_status

logger = logging.getLogger("bloomberg_mcp")
logging.basicConfig(level=logging.INFO)


# ======================================================================
# Lifespan — shared BloombergClient instance
# ======================================================================

@asynccontextmanager
async def lifespan(server: FastMCP):
    """Create a shared BloombergClient for the server lifetime."""
    client = BloombergClient()
    yield {"bloomberg": client}


mcp = FastMCP(
    "Bloomberg",
    instructions=(
        "Bloomberg Terminal data access — BDP, BDH, BDIB, BQL queries, "
        "bond analytics, screening, field search, and charting."
    ),
    lifespan=lifespan,
)


# ======================================================================
# Helpers
# ======================================================================

def _error_response(error: str, error_type: str = "error", suggestion: str | None = None) -> dict[str, Any]:
    resp: dict[str, Any] = {"error": error, "type": error_type}
    if suggestion:
        resp["suggestion"] = suggestion
    return resp


def _get_client(ctx: Context) -> BloombergClient:
    return ctx.lifespan_context["bloomberg"]


# ======================================================================
# Pydantic input models
# ======================================================================

class BdpInput(BaseModel):
    securities: list[str] = Field(..., min_length=1, description="Bloomberg tickers, e.g. ['AAPL US Equity']")
    fields: list[str] = Field(..., min_length=1, description="Bloomberg field mnemonics, e.g. ['PX_LAST']")
    overrides: dict[str, str] | None = Field(None, description="Optional field overrides")


class BdhInput(BaseModel):
    securities: list[str] = Field(..., min_length=1)
    fields: list[str] = Field(..., min_length=1)
    start_date: str = Field(..., description="Start date YYYY-MM-DD")
    end_date: str | None = Field(None, description="End date YYYY-MM-DD (default: today)")
    periodicity: str | None = Field(None, description="D, W, M, Q, Y")
    adjust: str | None = Field(None, description="Adjustment: all, split, etc.")

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def _validate_date(cls, v):
        if v is None:
            return v
        v = str(v).strip()
        if len(v) == 10 and v[4] == "-" and v[7] == "-":
            return v
        raise ValueError(f"Date must be YYYY-MM-DD, got: {v}")


class BdibInput(BaseModel):
    security: str = Field(..., description="Single Bloomberg ticker")
    date: str = Field(..., description="Trading date YYYY-MM-DD")
    interval: int = Field(5, ge=1, le=1440, description="Bar interval in minutes")
    session: str = Field("allday", description="Session: allday, day, am, pm, etc.")


class BqlInput(BaseModel):
    query: str = Field(..., min_length=5, description="BQL query string")
    validate_first: bool = Field(True, description="Validate syntax before executing")


class BqlBuildInput(BaseModel):
    intent: str = Field(..., description="Natural-language description of desired query")
    universe_type: str | None = Field(None, description="equity, bond, index, or loan")


class BondInfoInput(BaseModel):
    securities: list[str] = Field(..., min_length=1)
    include_risk: bool = Field(True, description="Include duration, convexity, DV01")
    include_spreads: bool = Field(True, description="Include OAS, Z-spread, ASW")


class ScreenInput(BaseModel):
    screen_name: str | None = Field(None, description="Saved Bloomberg screen name")
    bql_filter: str | None = Field(None, description="Ad-hoc BQL filter expression")
    fields: list[str] = Field(default_factory=lambda: ["name", "px_last"], description="Fields to retrieve")
    max_results: int = Field(100, ge=1, le=5000)


class FieldSearchInput(BaseModel):
    query: str = Field(..., min_length=2, description="Search term for field mnemonics")
    max_results: int = Field(20, ge=1, le=100)


# ======================================================================
# Tool 1: bloomberg_status
# ======================================================================

@mcp.tool()
async def bloomberg_status() -> dict[str, Any]:
    """Check Bloomberg Terminal connectivity and API status.

    Returns process list, terminal_running flag, and api_connected flag.
    No arguments required.
    """
    return await asyncio.to_thread(check_bloomberg_status)


# ======================================================================
# Tool 2: bloomberg_bdp
# ======================================================================

@mcp.tool()
async def bloomberg_bdp(securities: list[str], fields: list[str], overrides: dict[str, str] | None = None, ctx: Context = None) -> dict[str, Any]:
    """Fetch Bloomberg reference/snapshot data (BDP).

    Returns current values for specified fields across one or more securities.
    Example: securities=["AAPL US Equity"], fields=["PX_LAST", "Security_Name"]
    """
    try:
        inp = BdpInput(securities=securities, fields=fields, overrides=overrides)
    except Exception as e:
        return _error_response(str(e), "validation_error")

    try:
        client = _get_client(ctx)
        return await asyncio.to_thread(client.bdp, inp.securities, inp.fields, inp.overrides)
    except Exception as e:
        return _error_response(str(e), "bloomberg_error", "Ensure Bloomberg Terminal is running")


# ======================================================================
# Tool 3: bloomberg_bdh
# ======================================================================

@mcp.tool()
async def bloomberg_bdh(
    securities: list[str],
    fields: list[str],
    start_date: str,
    end_date: str | None = None,
    periodicity: str | None = None,
    adjust: str | None = None,
    ctx=None,
) -> dict[str, Any]:
    """Fetch Bloomberg historical time series data (BDH).

    Returns end-of-day values over a date range.
    Example: securities=["SPY US Equity"], fields=["PX_LAST"], start_date="2024-01-01"
    Periodicity options: D (daily), W (weekly), M (monthly), Q (quarterly), Y (yearly)
    """
    try:
        inp = BdhInput(securities=securities, fields=fields, start_date=start_date, end_date=end_date, periodicity=periodicity, adjust=adjust)
    except Exception as e:
        return _error_response(str(e), "validation_error")

    try:
        client = _get_client(ctx)
        return await asyncio.to_thread(client.bdh, inp.securities, inp.fields, inp.start_date, inp.end_date, inp.periodicity, inp.adjust)
    except Exception as e:
        return _error_response(str(e), "bloomberg_error", "Ensure Bloomberg Terminal is running")


# ======================================================================
# Tool 4: bloomberg_bdib
# ======================================================================

@mcp.tool()
async def bloomberg_bdib(
    security: str,
    date: str,
    interval: int = 5,
    session: str = "allday",
    ctx=None,
) -> dict[str, Any]:
    """Fetch Bloomberg intraday bar data (BDIB).

    Returns OHLCV bars at specified minute intervals for a single trading day.
    Example: security="SPY US Equity", date="2024-01-15", interval=5
    """
    try:
        inp = BdibInput(security=security, date=date, interval=interval, session=session)
    except Exception as e:
        return _error_response(str(e), "validation_error")

    try:
        client = _get_client(ctx)
        return await asyncio.to_thread(client.bdib, inp.security, inp.date, inp.interval, inp.session)
    except Exception as e:
        return _error_response(str(e), "bloomberg_error", "Ensure Bloomberg Terminal is running")


# ======================================================================
# Tool 5: bloomberg_bql
# ======================================================================

@mcp.tool()
async def bloomberg_bql(query: str, validate_first: bool = True, ctx: Context = None) -> dict[str, Any]:
    """Execute a Bloomberg Query Language (BQL) query.

    BQL is Bloomberg's most powerful query interface. Supports screening,
    aggregation, time series, and cross-entity analysis.

    Example: query="get(px_last) for(['IBM US Equity'])"
    Set validate_first=False to skip syntax validation.
    """
    try:
        inp = BqlInput(query=query, validate_first=validate_first)
    except Exception as e:
        return _error_response(str(e), "validation_error")

    if inp.validate_first:
        validation = validate_bql(inp.query)
        if not validation["valid"]:
            return _error_response(
                "BQL syntax issues detected",
                "validation_error",
                suggestion="; ".join(validation["issues"]),
            )

    try:
        client = _get_client(ctx)
        return await asyncio.to_thread(client.bql, inp.query)
    except Exception as e:
        return _error_response(str(e), "bloomberg_error", "Check BQL syntax and Bloomberg connectivity")


# ======================================================================
# Tool 6: bloomberg_bql_build
# ======================================================================

@mcp.tool()
async def bloomberg_bql_build(intent: str, universe_type: str | None = None) -> dict[str, Any]:
    """Build a BQL query template from a natural-language description.

    Returns a template, defaults, syntax rules, and examples.
    Does NOT require Bloomberg Terminal — pure local logic.

    Example: intent="screen investment-grade USD bonds", universe_type="bond"
    """
    try:
        inp = BqlBuildInput(intent=intent, universe_type=universe_type)
    except Exception as e:
        return _error_response(str(e), "validation_error")

    return build_bql_from_intent(inp.intent, inp.universe_type)


# ======================================================================
# Tool 7: bloomberg_bond_info
# ======================================================================

@mcp.tool()
async def bloomberg_bond_info(
    securities: list[str],
    include_risk: bool = True,
    include_spreads: bool = True,
    ctx=None,
) -> dict[str, Any]:
    """Fetch fixed income analytics for bonds.

    Returns coupon, maturity, price, yield, and optionally duration/convexity/DV01
    and OAS/Z-spread/ASW.

    Example: securities=["T 4.5 05/15/38 Govt"]
    Use /cusip/ or /isin/ prefixes: securities=["/cusip/912810TD8"]
    """
    try:
        inp = BondInfoInput(securities=securities, include_risk=include_risk, include_spreads=include_spreads)
    except Exception as e:
        return _error_response(str(e), "validation_error")

    try:
        client = _get_client(ctx)
        return await asyncio.to_thread(client.bond_info, inp.securities, inp.include_risk, inp.include_spreads)
    except Exception as e:
        return _error_response(str(e), "bloomberg_error", "Ensure Bloomberg Terminal is running")


# ======================================================================
# Tool 8: bloomberg_screen
# ======================================================================

@mcp.tool()
async def bloomberg_screen(
    screen_name: str | None = None,
    bql_filter: str | None = None,
    fields: list[str] | None = None,
    max_results: int = 100,
    ctx=None,
) -> dict[str, Any]:
    """Screen securities using a saved Bloomberg screen or ad-hoc BQL filter.

    Provide EITHER screen_name (for saved BEQS screens) OR bql_filter (ad-hoc).

    Example (saved): screen_name="MyInvestmentGradeScreen"
    Example (ad-hoc): bql_filter="crncy=='USD' and rtg_sp() in ['A+','A','A-']",
                      fields=["name", "yield()", "spread()"]
    """
    fields = fields or ["name", "px_last"]
    try:
        inp = ScreenInput(screen_name=screen_name, bql_filter=bql_filter, fields=fields, max_results=max_results)
    except Exception as e:
        return _error_response(str(e), "validation_error")

    if not inp.screen_name and not inp.bql_filter:
        return _error_response("Provide either screen_name or bql_filter", "validation_error")

    try:
        client = _get_client(ctx)
        if inp.screen_name:
            return await asyncio.to_thread(client.screen_eqs, inp.screen_name)
        else:
            return await asyncio.to_thread(client.screen_bql, inp.bql_filter, inp.fields, inp.max_results)
    except Exception as e:
        return _error_response(str(e), "bloomberg_error", "Ensure Bloomberg Terminal is running")


# ======================================================================
# Tool 9: bloomberg_field_search
# ======================================================================

@mcp.tool()
async def bloomberg_field_search(query: str, max_results: int = 20, ctx: Context = None) -> dict[str, Any]:
    """Search Bloomberg field mnemonics by keyword.

    Helps discover the correct field names for BDP/BDH/BQL queries.
    Example: query="yield to maturity"
    """
    try:
        inp = FieldSearchInput(query=query, max_results=max_results)
    except Exception as e:
        return _error_response(str(e), "validation_error")

    try:
        client = _get_client(ctx)
        results = await asyncio.to_thread(client.field_search, inp.query, inp.max_results)
        return {"fields": results, "count": len(results), "query": inp.query}
    except Exception as e:
        return _error_response(str(e), "bloomberg_error", "Ensure Bloomberg Terminal is running")
