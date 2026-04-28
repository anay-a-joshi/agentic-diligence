"""SEC EDGAR fetcher using edgartools."""
from typing import Any
from edgar import set_identity, Company

from app.config import settings
from app.utils.logger import logger


def _ensure_identity():
    """edgartools requires identity for SEC compliance."""
    set_identity(settings.sec_user_agent)


def fetch_company_filings(ticker: str) -> dict[str, Any]:
    """Fetch the most recent filings for a public company.

    Returns a dict with:
      - company_name
      - cik
      - filings_summary (counts by form type)
      - _latest_10k_obj  (edgar Filing object, used by FinancialAgent)
      - _latest_10q_obj
      - _latest_def14a_obj
      - recent_8k_objs (list)
    """
    _ensure_identity()

    try:
        company = Company(ticker)
    except Exception as e:
        logger.error(f"Could not resolve ticker {ticker}: {e}")
        raise

    company_name = company.name
    cik = str(company.cik)

    filings_10k = company.get_filings(form="10-K").head(3)
    filings_10q = company.get_filings(form="10-Q").head(4)
    filings_8k = company.get_filings(form="8-K").head(10)
    filings_def14a = company.get_filings(form="DEF 14A").head(2)

    return {
        "company_name": company_name,
        "cik": cik,
        "filings_summary": {
            "10K": len(filings_10k),
            "10Q": len(filings_10q),
            "8K": len(filings_8k),
            "DEF14A": len(filings_def14a),
        },
        "_latest_10k_obj": filings_10k[0] if len(filings_10k) > 0 else None,
        "_latest_10q_obj": filings_10q[0] if len(filings_10q) > 0 else None,
        "_latest_def14a_obj": filings_def14a[0] if len(filings_def14a) > 0 else None,
        "recent_8k_objs": list(filings_8k) if len(filings_8k) > 0 else [],
    }


def get_filing_text(filing_obj, max_chars: int = 35_000) -> str:
    """Extract plain text from a filing object, capped at max_chars.

    Tries to grab the most financially-dense section first (MD&A or
    financial statements) before falling back to raw text.
    """
    if filing_obj is None:
        return ""

    # Strategy 1: Try to extract specific 10-K items via the Filing.obj() Form10K helper
    try:
        form_obj = filing_obj.obj()
        # edgartools Form10K exposes named items
        # Item 7 = MD&A (revenue discussion), Item 8 = Financial Statements
        for item_name in ["Item 7", "Item 7A", "Item 8"]:
            try:
                item_text = getattr(form_obj, item_name.replace(" ", "_").lower(), None)
                if item_text:
                    text = str(item_text)
                    if len(text) > 1000:  # sanity check
                        logger.info(f"  Got {item_name} via Form10K helper ({len(text)} chars)")
                        return text[:max_chars]
            except Exception:
                pass
    except Exception:
        pass

    # Strategy 2: Search raw text for MD&A heading and slice from there
    try:
        full_text = filing_obj.text() if hasattr(filing_obj, "text") else str(filing_obj)
    except Exception as e:
        logger.warning(f"  Could not get filing text: {e}")
        return ""

    if not full_text:
        return ""

    # Common MD&A heading variations in 10-Ks
    mda_markers = [
        "Management's Discussion and Analysis",
        "MANAGEMENT'S DISCUSSION AND ANALYSIS",
        "Item 7.",
        "ITEM 7.",
        "Results of Operations",
        "RESULTS OF OPERATIONS",
    ]

    for marker in mda_markers:
        idx = full_text.find(marker)
        if idx > 0:
            # Found MD&A — slice from here forward
            sliced = full_text[idx : idx + max_chars]
            logger.info(f"  Found '{marker}' at offset {idx}, slicing {len(sliced)} chars")
            return sliced

    # Fallback: just return the first chunk
    logger.info(f"  No MD&A marker found, returning first {max_chars} chars")
    return full_text[:max_chars]
