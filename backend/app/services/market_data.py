"""Pulls market data via yfinance (free, no API key)."""
from typing import Any
import yfinance as yf

from app.utils.logger import logger


def fetch_market_data(ticker: str) -> dict[str, Any]:
    """Get current price, market cap, P/E, 52-week range, beta."""
    try:
        t = yf.Ticker(ticker)
        info = t.info or {}

        out = {
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "market_cap_usd_millions": (
                round(info.get("marketCap", 0) / 1_000_000) if info.get("marketCap") else None
            ),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "ev_usd_millions": (
                round(info.get("enterpriseValue", 0) / 1_000_000)
                if info.get("enterpriseValue") else None
            ),
            "ev_to_ebitda": info.get("enterpriseToEbitda"),
            "ev_to_revenue": info.get("enterpriseToRevenue"),
            "beta": info.get("beta"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "dividend_yield_pct": (
                round(info.get("dividendYield", 0) * 100, 2)
                if info.get("dividendYield") else None
            ),
            "shares_outstanding_millions": (
                round(info.get("sharesOutstanding", 0) / 1_000_000)
                if info.get("sharesOutstanding") else None
            ),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
        }
        logger.info(
            f"  Market: ${out.get('current_price')}, "
            f"mkt cap ${out.get('market_cap_usd_millions')}M, "
            f"P/E {out.get('pe_ratio')}, beta {out.get('beta')}"
        )
        return out
    except Exception as e:
        logger.warning(f"  yfinance fetch failed: {e}")
        return {}
