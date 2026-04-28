"""Orchestrator — runs all 7 specialist agents sequentially."""
from typing import Any

from app.agents.financial_agent import FinancialAgent
from app.agents.commercial_agent import CommercialAgent
from app.agents.risk_agent import RiskAgent
from app.agents.governance_agent import GovernanceAgent
from app.agents.market_agent import MarketAgent
from app.agents.sentiment_agent import SentimentAgent
from app.agents.red_flag_agent import RedFlagAgent

from app.models.analysis import AnalysisResult, FinancialData
from app.services.sec_edgar import fetch_company_filings
from app.utils.logger import logger


def _coerce_lists(data: dict) -> dict:
    """Coerce null lists to []. LLMs sometimes return null instead."""
    for field in ("key_drivers", "key_risks", "non_recurring_items"):
        if data.get(field) is None:
            data[field] = []
    if data.get("summary") is None:
        data["summary"] = ""
    return data


async def run_full_analysis(ticker: str) -> AnalysisResult:
    """Run the full multi-agent diligence pipeline."""
    ticker = ticker.upper().strip()
    logger.info(f"🎯 Starting analysis for {ticker}")
    logger.info(f"📥 Fetching SEC filings for {ticker}")

    bundle = fetch_company_filings(ticker)
    bundle["cik"] = bundle["cik"]  # ensure cik accessible to agents

    company_name = bundle["company_name"]
    cik = bundle["cik"]
    filings_summary = bundle["filings_summary"]

    raw_findings: dict[str, Any] = {}
    financial: FinancialData | None = None

    # Run all 7 agents sequentially
    agent_classes = [
        FinancialAgent,
        CommercialAgent,
        RiskAgent,
        GovernanceAgent,
        MarketAgent,
        SentimentAgent,
        RedFlagAgent,
    ]

    for AgentClass in agent_classes:
        agent = AgentClass(ticker=ticker, filings=bundle)
        try:
            result = await agent.run()
            raw_findings[agent.name] = result
        except Exception as e:
            logger.warning(f"Agent {agent.name} crashed: {e}")
            raw_findings[agent.name] = {"status": "error", "error": str(e), "data": None}

    # Build typed FinancialData from financial_agent output
    fa_result = raw_findings.get("financial_agent", {})
    if fa_result.get("status") == "ok" and fa_result.get("data"):
        try:
            cleaned = _coerce_lists(dict(fa_result["data"]))
            financial = FinancialData(**cleaned)
        except Exception as e:
            logger.warning(f"Could not parse FinancialData: {e}")

    # Aggregate red flags from RedFlagAgent for top-level view
    red_flags_top: list[str] = []
    rf_data = raw_findings.get("red_flag_agent", {}).get("data") or {}
    for flag in rf_data.get("red_flags", []) or []:
        if str(flag.get("severity", "")).lower() in ("high", "critical"):
            red_flags_top.append(f"[{flag.get('severity')}] {flag.get('flag')}: {flag.get('description', '')[:120]}")

    logger.info(f"✅ Analysis complete: {len([k for k, v in raw_findings.items() if v.get('status') == 'ok'])}/7 agents OK")

    return AnalysisResult(
        ticker=ticker,
        company_name=company_name,
        cik=cik,
        filings_summary=filings_summary,
        financial=financial,
        red_flags=red_flags_top,
        raw_findings=raw_findings,
    )
