"""SEC EDGAR client — fetches 10-K, 10-Q, 8-K, DEF 14A filings using edgartools."""
from typing import Any
import asyncio

from edgar import Company, set_identity

from app.config import settings
from app.utils.logger import logger


# Initialize edgartools with the SEC-required User-Agent identity
_identity_set = False


def _ensure_identity():
    """SEC requires a User-Agent identifying the requester. Set once."""
    global _identity_set
    if not _identity_set:
        set_identity(settings.sec_user_agent)
        _identity_set = True


def _fetch_sync(ticker: str) -> dict[str, Any]:
    """Blocking SEC fetch — wrapped in a thread for async use."""
    _ensure_identity()

    logger.info(f"📥 Fetching SEC filings for {ticker}")
    company = Company(ticker)

    # Pull recent filings
    filings_10k = company.get_filings(form="10-K").head(3)  # last 3 annuals
    filings_10q = company.get_filings(form="10-Q").head(4)  # last 4 quarters
    filings_8k = company.get_filings(form="8-K").head(10)   # last 10 material events
    filings_def14a = company.get_filings(form="DEF 14A").head(2)  # last 2 proxies

    def _serialize(filings) -> list[dict]:
        results = []
        for f in filings:
            try:
                results.append({
                    "form": f.form,
                    "filing_date": str(f.filing_date),
                    "accession_number": f.accession_no,
                    "url": f.homepage_url if hasattr(f, "homepage_url") else "",
                })
            except Exception as e:
                logger.warning(f"Could not serialize filing: {e}")
        return results

    return {
        "ticker": ticker,
        "company_name": company.name if hasattr(company, "name") else ticker,
        "cik": str(company.cik) if hasattr(company, "cik") else "",
        "10K": _serialize(filings_10k),
        "10Q": _serialize(filings_10q),
        "8K": _serialize(filings_8k),
        "DEF14A": _serialize(filings_def14a),
        # Also keep the latest 10-K filing object for deep extraction by agents
        "_latest_10k_obj": filings_10k[0] if len(filings_10k) > 0 else None,
        "_latest_10q_obj": filings_10q[0] if len(filings_10q) > 0 else None,
    }


async def fetch_company_filings(ticker: str) -> dict[str, Any]:
    """Async wrapper around the blocking SEC client."""
    return await asyncio.to_thread(_fetch_sync, ticker)


def get_filing_text(filing_obj, max_chars: int = 200_000) -> str:
    """
    Extract the textual content of a filing for LLM consumption.
    Truncates to max_chars to stay within Gemini's free-tier context budget.
    """
    if filing_obj is None:
        return ""
    try:
        # edgartools exposes .text() on filings
        text = filing_obj.text() if hasattr(filing_obj, "text") else str(filing_obj)
        return text[:max_chars]
    except Exception as e:
        logger.warning(f"Could not extract filing text: {e}")
        return ""
