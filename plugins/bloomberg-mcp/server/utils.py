"""
Utility helpers for the Bloomberg MCP server.

- Bloomberg Terminal connectivity check
- Identifier conversion (CUSIP/ISIN to ticker)
- DataFrame serialization
- Field search wrapper
"""

from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any


def check_bloomberg_status() -> dict[str, Any]:
    """Check if Bloomberg Terminal processes are running and test a BDP call."""
    status: dict[str, Any] = {
        "terminal_running": False,
        "api_connected": False,
        "processes": [],
        "error": None,
    }

    try:
        import psutil

        bbg_names = {"wintrv.exe", "bbcomm.exe", "bblauncher.exe", "bbg.exe"}
        for proc in psutil.process_iter(["name"]):
            name = (proc.info["name"] or "").lower()
            if name in bbg_names:
                status["processes"].append(name)
        status["terminal_running"] = len(status["processes"]) > 0
    except ImportError:
        status["error"] = "psutil not installed"
        return status
    except Exception as exc:
        status["error"] = f"Process check failed: {exc}"

    if not status["terminal_running"]:
        status["error"] = "No Bloomberg Terminal processes detected"
        return status

    try:
        from xbbg import blp

        df = blp.bdp("IBM US Equity", "PX_LAST")
        if df is not None and not df.empty:
            status["api_connected"] = True
        else:
            status["error"] = "BDP call returned empty result"
    except Exception as exc:
        status["error"] = f"API connection test failed: {exc}"

    return status


def cusip_to_ticker(cusip: str) -> str:
    """Convert a CUSIP identifier to a Bloomberg ticker via BDP."""
    from xbbg import blp

    df = blp.bdp(f"/cusip/{cusip}", "PARSEKYABLE_DES")
    if df is not None and not df.empty:
        return str(df.iloc[0, 0])
    return f"/cusip/{cusip}"


def isin_to_ticker(isin: str) -> str:
    """Convert an ISIN identifier to a Bloomberg ticker via BDP."""
    from xbbg import blp

    df = blp.bdp(f"/isin/{isin}", "PARSEKYABLE_DES")
    if df is not None and not df.empty:
        return str(df.iloc[0, 0])
    return f"/isin/{isin}"


class _JSONEncoder(json.JSONEncoder):
    """Handle dates, datetimes, and other non-JSON-native types."""

    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        try:
            import numpy as np

            if isinstance(o, (np.integer,)):
                return int(o)
            if isinstance(o, (np.floating,)):
                return float(o)
            if isinstance(o, np.ndarray):
                return o.tolist()
        except ImportError:
            pass
        return super().default(o)


def serialize_dataframe(df: Any) -> dict[str, Any]:
    """Serialize a pandas or polars DataFrame to a JSON-ready dict."""
    try:
        import polars as pl

        if isinstance(df, pl.DataFrame):
            records = df.to_dicts()
            clean = json.loads(json.dumps(records, cls=_JSONEncoder))
            return {
                "data": clean,
                "columns": df.columns,
                "shape": list(df.shape),
            }
    except ImportError:
        pass

    try:
        import pandas as pd

        if isinstance(df, pd.DataFrame):
            if isinstance(df.columns, pd.MultiIndex):
                df = df.copy()
                df.columns = [
                    "|".join(str(c) for c in col).strip("|")
                    for col in df.columns.values
                ]

            if df.index.name or not isinstance(df.index, pd.RangeIndex):
                df = df.reset_index()

            records = json.loads(
                df.to_json(orient="records", date_format="iso", default_handler=str)
            )
            return {
                "data": records,
                "columns": list(df.columns),
                "shape": list(df.shape),
            }
    except ImportError:
        pass

    return {"data": [], "columns": [], "shape": [0, 0], "error": "Unsupported type"}


def search_fields(query: str, max_results: int = 20) -> list[dict[str, str]]:
    """Search Bloomberg field mnemonics via ``blp.fieldSearch``."""
    from xbbg import blp

    df = blp.fieldSearch(query)
    if df is None or df.empty:
        return []

    df = df.head(max_results)
    return serialize_dataframe(df)["data"]
