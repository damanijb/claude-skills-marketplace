"""
Unified Bloomberg data access layer.

Wraps xbbg and polars-bloomberg behind a single ``BloombergClient`` class.
All methods return JSON-serializable dicts via ``utils.serialize_dataframe``.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from utils import serialize_dataframe

logger = logging.getLogger("bloomberg_mcp")


class BloombergClient:
    """Single shared instance created during server lifespan."""

    def __init__(self) -> None:
        self._blp = None  # lazy xbbg.blp
        self._bquery_cls = None  # lazy polars_bloomberg.BQuery

    # ------------------------------------------------------------------
    # Lazy imports
    # ------------------------------------------------------------------

    @property
    def blp(self):
        if self._blp is None:
            from xbbg import blp

            self._blp = blp
        return self._blp

    @property
    def bquery_cls(self):
        if self._bquery_cls is None:
            from polars_bloomberg import BQuery

            self._bquery_cls = BQuery
        return self._bquery_cls

    # ------------------------------------------------------------------
    # BDP — Reference / Snapshot Data
    # ------------------------------------------------------------------

    def bdp(
        self,
        securities: list[str],
        fields: list[str],
        overrides: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        kwargs: dict[str, Any] = {}
        if overrides:
            kwargs.update(overrides)
        df = self.blp.bdp(tickers=securities, flds=fields, **kwargs)
        return serialize_dataframe(df)

    # ------------------------------------------------------------------
    # BDH — Historical Time Series
    # ------------------------------------------------------------------

    def bdh(
        self,
        securities: list[str],
        fields: list[str],
        start_date: str,
        end_date: str | None = None,
        periodicity: str | None = None,
        adjust: str | None = None,
    ) -> dict[str, Any]:
        end_date = end_date or datetime.now().strftime("%Y-%m-%d")
        kwargs: dict[str, Any] = {}
        if periodicity:
            kwargs["Per"] = periodicity
        if adjust:
            kwargs["adjust"] = adjust
        df = self.blp.bdh(
            tickers=securities,
            flds=fields,
            start_date=start_date,
            end_date=end_date,
            **kwargs,
        )
        return serialize_dataframe(df)

    # ------------------------------------------------------------------
    # BDIB — Intraday Bars
    # ------------------------------------------------------------------

    def bdib(
        self,
        security: str,
        date: str,
        interval: int = 5,
        session: str = "allday",
    ) -> dict[str, Any]:
        df = self.blp.bdib(ticker=security, dt=date, interval=interval, session=session)
        return serialize_dataframe(df)

    # ------------------------------------------------------------------
    # BQL — Bloomberg Query Language
    # ------------------------------------------------------------------

    def bql(self, query: str) -> dict[str, Any]:
        """Execute a BQL query.  Prefer polars-bloomberg, fall back to xbbg."""
        try:
            bq_cls = self.bquery_cls
            with bq_cls() as bq:
                results = bq.bql(query)
                df = results.combine()
                return serialize_dataframe(df)
        except ImportError:
            logger.info("polars-bloomberg not available, falling back to xbbg BQL")
        except Exception as exc:
            logger.warning("polars-bloomberg BQL failed (%s), trying xbbg", exc)

        df = self.blp.bql(query)
        return serialize_dataframe(df)

    # ------------------------------------------------------------------
    # Bond Info — Fixed Income Analytics
    # ------------------------------------------------------------------

    def bond_info(
        self,
        securities: list[str],
        include_risk: bool = True,
        include_spreads: bool = True,
    ) -> dict[str, Any]:
        """Fetch bond reference data plus optional risk/spread analytics."""
        base_fields = [
            "SECURITY_NAME",
            "COUPON",
            "MATURITY",
            "ISSUE_DT",
            "CRNCY",
            "AMT_OUTSTANDING",
            "PX_LAST",
            "YLD_YTM_MID",
        ]
        if include_risk:
            base_fields += ["DUR_ADJ_MID", "DUR_ADJ_OAS_MID", "CONVEXITY_MID", "DV01"]
        if include_spreads:
            base_fields += ["OAS_SPREAD_MID", "Z_SPRD_MID", "ASSET_SWAP_SPD_MID"]

        df = self.blp.bdp(tickers=securities, flds=base_fields)
        return serialize_dataframe(df)

    # ------------------------------------------------------------------
    # Screening
    # ------------------------------------------------------------------

    def screen_eqs(self, screen_name: str) -> dict[str, Any]:
        """Run a saved Bloomberg equity screen (BEQS)."""
        df = self.blp.beqs(screen=screen_name)
        return serialize_dataframe(df)

    def screen_bql(
        self,
        bql_filter: str,
        fields: list[str],
        max_results: int = 100,
    ) -> dict[str, Any]:
        """Ad-hoc screening via BQL filter expression."""
        fields_str = ", ".join(fields)
        query = f"get({fields_str}) for(filter(bondsUniv('active'), {bql_filter}))"
        result = self.bql(query)
        if result.get("data") and len(result["data"]) > max_results:
            result["data"] = result["data"][:max_results]
            result["shape"][0] = max_results
            result["truncated"] = True
        return result

    # ------------------------------------------------------------------
    # Field Search
    # ------------------------------------------------------------------

    def field_search(self, query: str, max_results: int = 20) -> list[dict[str, str]]:
        """Search Bloomberg field mnemonics."""
        from utils import search_fields

        return search_fields(query, max_results=max_results)
