"""Orchestrator — runs all agents, packages the AnalysisResult."""
from typing import Any

from app.agents.financial_agent import FinancialAgent
from app.models.analysis import AnalysisResult, FinancialData
from app.services.sec_edgar import fetch_company_filings
from app.utils.logger import logger


def _coerce_lists(data: dict) -> dict:
    """LLMs sometimes return null instead of an empty list. Coerce to [] for list fields."""
    for field in ("key_drivers", "key_risks", "non_recurring_items"):
        if field in data and data[field] is None:
            data[field] = []
    if data.get("summary") is None:
        data["summary"] = ""
    return data


async def run_full_analysis(ticker: str) -> AnalysisResult:
    """Run the multi-agent pipeline for a ticker."""
    ticker = ticker.upper().strip()
    logger.info(f"🎯 Starting analysis for {ticker}")
    logger.info(f"📥 Fetching SEC filings for {ticker}")

    bundle = fetch_company_filings(ticker)

    company_name = bundle["company_name"]
    cik = bundle["cik"]
    filings_summary = bundle["filings_summary"]

    raw_findings: dict[str, Any] = {}
    financial: FinancialData | None = None

    # Phase 1: Financial Agent only. Other 6 agents come in Phase 2.
    fa = FinancialAgent(ticker=ticker, filings=bundle)
    fa_result = await fa.run()
    raw_findings["financial_agent"] = fa_result

    if fa_result.get("status") == "ok" and fa_result.get("data"):
        try:
            cleaned = _coerce_lists(dict(fa_result["data"]))
            financial = FinancialData(**cleaned)
        except Exception as e:
            logger.warning(f"Could not parse FinancialData: {e}")

    return AnalysisResult(
        ticker=ticker,
        company_name=company_name,
        cik=cik,
        filings_summary=filings_summary,
        financial=financial,
        raw_findings=raw_findings,
    )
