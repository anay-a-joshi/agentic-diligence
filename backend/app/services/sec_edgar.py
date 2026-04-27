"""SEC EDGAR client — fetches 10-K, 10-Q, 8-K, DEF 14A filings."""
from typing import Any

from app.config import settings
from app.utils.logger import logger


async def fetch_company_filings(ticker: str) -> dict[str, Any]:
    """
    Fetch the most recent filings for a ticker.
    Uses edgartools (free) under the hood.
    """
    logger.info(f"📥 Fetching SEC filings for {ticker}")
    # TODO: implement using edgartools
    # from edgar import Company, set_identity
    # set_identity(settings.sec_user_agent)
    # company = Company(ticker)
    # filings_10k = company.get_filings(form="10-K").latest(5)
    # ...
    return {
        "ticker": ticker,
        "10K": [],
        "10Q": [],
        "8K": [],
        "DEF14A": [],
    }
