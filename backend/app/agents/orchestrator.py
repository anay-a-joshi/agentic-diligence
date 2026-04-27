"""Orchestrator coordinates all specialist agents.
Phase 1: only Financial Agent is wired up. Other phases will add the rest.
"""
import asyncio

from app.agents.financial_agent import FinancialAgent
from app.services.sec_edgar import fetch_company_filings
from app.models.analysis import AnalysisResult, FinancialData
from app.utils.logger import logger


async def run_full_analysis(ticker: str) -> AnalysisResult:
    """Master pipeline. Returns an AnalysisResult populated with whatever phase has built."""
    ticker = ticker.upper()
    logger.info(f"🎯 Starting analysis for {ticker}")

    # Step 1: Fetch all filings
    filings = await fetch_company_filings(ticker)

    # Step 2: Run agents (Phase 1 = just Financial)
    financial_result = await FinancialAgent(ticker, filings).run()

    # Build response
    financial = None
    if financial_result.get("status") == "ok" and financial_result.get("data"):
        try:
            financial = FinancialData(**financial_result["data"])
        except Exception as e:
            logger.warning(f"Could not parse FinancialData: {e}")

    return AnalysisResult(
        ticker=ticker,
        company_name=filings.get("company_name", ticker),
        cik=filings.get("cik", ""),
        filings_summary={
            "10K": len(filings.get("10K", [])),
            "10Q": len(filings.get("10Q", [])),
            "8K": len(filings.get("8K", [])),
            "DEF14A": len(filings.get("DEF14A", [])),
        },
        financial=financial,
        raw_findings={"financial_agent": financial_result},
    )
