"""SEC EDGAR fetcher using edgartools."""
from typing import Any
from edgar import set_identity, Company

from app.config import settings
from app.utils.logger import logger


def _ensure_identity():
    set_identity(settings.sec_user_agent)


def fetch_company_filings(ticker: str) -> dict[str, Any]:
    _ensure_identity()
    try:
        company = Company(ticker)
    except Exception as e:
        logger.error(f"Could not resolve ticker {ticker}: {e}")
        raise

    filings_10k = company.get_filings(form="10-K").head(3)
    filings_10q = company.get_filings(form="10-Q").head(4)
    filings_8k = company.get_filings(form="8-K").head(10)
    filings_def14a = company.get_filings(form="DEF 14A").head(2)

    return {
        "company_name": company.name,
        "cik": str(company.cik),
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


def _slice_at_marker(text: str, markers: list[str], max_chars: int) -> str:
    """Find the first marker in text and return max_chars from there."""
    for marker in markers:
        idx = text.find(marker)
        if idx > 0:
            sliced = text[idx : idx + max_chars]
            logger.info(f"  Found '{marker}' at offset {idx}, slicing {len(sliced)} chars")
            return sliced
    logger.info(f"  No marker found, returning first {max_chars} chars")
    return text[:max_chars]


def _get_full_text(filing_obj) -> str:
    if filing_obj is None:
        return ""
    try:
        return filing_obj.text() if hasattr(filing_obj, "text") else str(filing_obj)
    except Exception as e:
        logger.warning(f"  Could not get filing text: {e}")
        return ""


def get_filing_text(filing_obj, max_chars: int = 35_000) -> str:
    """Get MD&A section of a 10-K (used by FinancialAgent)."""
    text = _get_full_text(filing_obj)
    if not text:
        return ""
    return _slice_at_marker(
        text,
        ["Management's Discussion and Analysis",
         "MANAGEMENT'S DISCUSSION AND ANALYSIS",
         "Item 7.", "ITEM 7.",
         "Results of Operations"],
        max_chars,
    )


def get_business_section(filing_obj, max_chars: int = 25_000) -> str:
    """Get Item 1 (Business) of a 10-K — for CommercialAgent."""
    text = _get_full_text(filing_obj)
    if not text:
        return ""
    return _slice_at_marker(
        text,
        ["Item 1.", "ITEM 1.", "Business Overview", "BUSINESS"],
        max_chars,
    )


def get_risk_factors(filing_obj, max_chars: int = 25_000) -> str:
    """Get Item 1A (Risk Factors) of a 10-K — for RiskAgent."""
    text = _get_full_text(filing_obj)
    if not text:
        return ""
    return _slice_at_marker(
        text,
        ["Item 1A.", "ITEM 1A.", "Risk Factors", "RISK FACTORS"],
        max_chars,
    )


def get_proxy_text(filing_obj, max_chars: int = 25_000) -> str:
    """Get text from a DEF 14A proxy — for GovernanceAgent."""
    text = _get_full_text(filing_obj)
    if not text:
        return ""
    # Proxies don't have standard items; just return the first chunk
    return text[:max_chars]


def get_recent_8k_text(filings_8k_list, max_chars: int = 20_000) -> str:
    """Concatenate text from recent 8-Ks — for RedFlagAgent."""
    if not filings_8k_list:
        return ""
    chunks = []
    remaining = max_chars
    for f in filings_8k_list[:5]:  # cap at 5 most recent
        if remaining <= 1000:
            break
        try:
            t = f.text() if hasattr(f, "text") else str(f)
            t_short = t[: min(4_000, remaining)]
            # Try to grab filing date if available
            date = getattr(f, "filing_date", "") or getattr(f, "date", "")
            chunks.append(f"=== 8-K filed {date} ===\n{t_short}\n")
            remaining -= len(t_short) + 100
        except Exception:
            continue
    return "\n".join(chunks)
