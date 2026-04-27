"""LangGraph orchestrator that coordinates all specialist agents."""
import asyncio
from typing import Any

from app.agents.financial_agent import FinancialAgent
from app.agents.commercial_agent import CommercialAgent
from app.agents.risk_agent import RiskAgent
from app.agents.governance_agent import GovernanceAgent
from app.agents.market_agent import MarketAgent
from app.agents.sentiment_agent import SentimentAgent
from app.agents.red_flag_agent import RedFlagAgent
from app.agents.synthesis_agent import SynthesisAgent
from app.services.sec_edgar import fetch_company_filings
from app.models.analysis import AnalysisResult
from app.utils.logger import logger


async def run_full_analysis(ticker: str) -> AnalysisResult:
    """Master pipeline: fetch filings → run agents in parallel → synthesize."""
    logger.info(f"🎯 Starting analysis for {ticker}")

    # Step 1: Fetch all filings
    filings = await fetch_company_filings(ticker)

    # Step 2: Spin up all specialist agents in parallel
    agents = [
        FinancialAgent(ticker, filings),
        CommercialAgent(ticker, filings),
        RiskAgent(ticker, filings),
        GovernanceAgent(ticker, filings),
        MarketAgent(ticker, filings),
        SentimentAgent(ticker, filings),
    ]
    results = await asyncio.gather(*[a.run() for a in agents])
    findings = {a.name: r for a, r in zip(agents, results)}

    # Step 3: Red flag cross-check
    red_flags = await RedFlagAgent(ticker, filings).cross_check(findings)

    # Step 4: Synthesize into final IC memo + score
    synthesis = await SynthesisAgent(ticker, filings).synthesize(findings, red_flags)

    return AnalysisResult(**synthesis)
