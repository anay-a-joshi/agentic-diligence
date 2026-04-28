"""Orchestrator — full Phase-3 pipeline with graceful degradation."""
import os
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
from app.services.lbo_engine import run_lbo_full
from app.services.feasibility_score import compute_feasibility
from app.generators.ic_memo_pdf import generate_ic_memo_pdf
from app.generators.lbo_excel import generate_lbo_excel

from app.models.analysis import AnalysisResult, FinancialData
from app.utils.logger import logger


OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "generated_outputs"))
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _coerce_lists(data: dict) -> dict:
    for field in ("key_drivers", "key_risks", "non_recurring_items"):
        if data.get(field) is None:
            data[field] = []
    if data.get("summary") is None:
        data["summary"] = ""
    return data


def _agent_data(raw: dict, key: str) -> dict | None:
    entry = raw.get(key) or {}
    if entry.get("status") in ("ok", "ok_fallback"):
        return entry.get("data") or {}
    return None


async def run_full_analysis(ticker: str) -> AnalysisResult:
    ticker = ticker.upper().strip()
    logger.info(f"🎯 Starting analysis for {ticker}")
    logger.info(f"📥 Fetching SEC filings for {ticker}")

    bundle = fetch_company_filings(ticker)
    company_name = bundle["company_name"]
    cik = bundle["cik"]
    filings_summary = bundle["filings_summary"]

    raw_findings: dict[str, Any] = {}

    agent_classes = [
        FinancialAgent, CommercialAgent, RiskAgent,
        GovernanceAgent, MarketAgent, SentimentAgent, RedFlagAgent,
    ]
    for AgentClass in agent_classes:
        agent = AgentClass(ticker=ticker, filings=bundle)
        try:
            result = await agent.run()
            raw_findings[agent.name] = result
        except Exception as e:
            logger.warning(f"Agent {agent.name} crashed: {e}")
            raw_findings[agent.name] = {"status": "error", "error": str(e), "data": None}

    fa = _agent_data(raw_findings, "financial_agent")
    market = _agent_data(raw_findings, "market_agent") or {}

    financial: FinancialData | None = None
    if fa:
        try:
            cleaned = _coerce_lists(dict(fa))
            financial = FinancialData(**cleaned)
        except Exception as e:
            logger.warning(f"Could not parse FinancialData: {e}")

    logger.info("💰 Running LBO model (base/bull/bear)...")
    try:
        lbo = run_lbo_full(
            financial=fa or {}, market=market,
            governance=_agent_data(raw_findings, "governance_agent"),
        )
        if lbo.get("status") == "ok":
            s = lbo["summary"]
            logger.info(f"  Base IRR: {s['irr_base_pct']}%, "
                        f"Bull IRR: {s['irr_bull_pct']}%, "
                        f"Bear IRR: {s['irr_bear_pct']}%")
        else:
            logger.warning("  LBO insufficient data")
    except Exception as e:
        logger.warning(f"  LBO crashed: {e}")
        lbo = {"status": "error", "error": str(e)}

    logger.info("🎯 Computing feasibility score...")
    try:
        feasibility = compute_feasibility(
            financial=fa,
            governance=_agent_data(raw_findings, "governance_agent"),
            risk=_agent_data(raw_findings, "risk_agent"),
            red_flag=_agent_data(raw_findings, "red_flag_agent"),
            sentiment=_agent_data(raw_findings, "sentiment_agent"),
            lbo=lbo if lbo.get("status") == "ok" else None,
        )
        logger.info(f"  Score: {feasibility['score']}/100 "
                    f"(Grade {feasibility['grade']}) — {feasibility['verdict']}")
    except Exception as e:
        logger.warning(f"  Feasibility scoring crashed: {e}")
        feasibility = {"score": 50, "grade": "C", "verdict": "Unable to score", "components": {}}

    logger.info("📝 Running synthesis agent...")
    try:
        synthesizer = SynthesisAgent(
            ticker=ticker, filings=bundle, all_findings=raw_findings,
            lbo_summary=lbo.get("summary", {}),
            feasibility=feasibility, company_name=company_name,
            financial=fa, market=market,
        )
        syn_result = await synthesizer.run()
    except Exception as e:
        logger.warning(f"Synthesis crashed: {e}")
        syn_result = {"status": "error", "error": str(e), "data": {}}
    raw_findings["synthesis_agent"] = syn_result
    synthesis_data = syn_result.get("data") or {}

    logger.info("📄 Generating IC memo PDF + LBO Excel...")
    pdf_path = ""
    xlsx_path = ""
    try:
        pdf_path = generate_ic_memo_pdf(
            ticker=ticker, company_name=company_name, output_dir=OUTPUT_DIR,
            financial=fa or {},
            commercial=_agent_data(raw_findings, "commercial_agent") or {},
            risk=_agent_data(raw_findings, "risk_agent") or {},
            governance=_agent_data(raw_findings, "governance_agent") or {},
            market=market,
            sentiment=_agent_data(raw_findings, "sentiment_agent") or {},
            red_flag=_agent_data(raw_findings, "red_flag_agent") or {},
            lbo=lbo, feasibility=feasibility, synthesis=synthesis_data,
        )
        logger.info(f"  ✅ IC memo: {pdf_path}")
    except Exception as e:
        logger.warning(f"  IC memo generation failed: {e}")

    try:
        xlsx_path = generate_lbo_excel(
            ticker=ticker, company_name=company_name, output_dir=OUTPUT_DIR,
            lbo=lbo, financial=fa or {}, market=market,
        )
        logger.info(f"  ✅ LBO Excel: {xlsx_path}")
    except Exception as e:
        logger.warning(f"  LBO Excel generation failed: {e}")

    red_flags_top: list[str] = []
    rf = _agent_data(raw_findings, "red_flag_agent") or {}
    for flag in rf.get("red_flags", []) or []:
        if str(flag.get("severity", "")).lower() in ("high", "critical"):
            red_flags_top.append(
                f"[{flag.get('severity')}] {flag.get('flag')}: "
                f"{(flag.get('description') or '')[:120]}"
            )

    ok_count = len([k for k, v in raw_findings.items()
                    if v.get("status") in ("ok", "ok_fallback")])
    logger.info(f"✅ Analysis complete: {ok_count}/{len(raw_findings)} agents OK "
                f"(others used fallback / rate-limited)")

    summary = lbo.get("summary", {}) if lbo.get("status") == "ok" else {}

    return AnalysisResult(
        ticker=ticker, company_name=company_name, cik=cik,
        filings_summary=filings_summary, financial=financial,
        feasibility_score=feasibility.get("score"),
        feasibility_grade=feasibility.get("grade"),
        feasibility_verdict=feasibility.get("verdict"),
        feasibility_breakdown=feasibility.get("components", {}),
        lbo_irr_base=summary.get("irr_base_pct"),
        lbo_irr_bull=summary.get("irr_bull_pct"),
        lbo_irr_bear=summary.get("irr_bear_pct"),
        lbo_moic_base=summary.get("moic_base"),
        lbo_full=lbo, synthesis=synthesis_data,
        red_flags=red_flags_top,
        ic_memo_url=f"/export/downloads/{os.path.basename(pdf_path)}" if pdf_path else "",
        lbo_excel_url=f"/export/downloads/{os.path.basename(xlsx_path)}" if xlsx_path else "",
        raw_findings=raw_findings,
    )


# ============================================================
# Cached wrapper — checks cache first, runs full analysis on miss
# ============================================================
from app.services.result_cache import load_cached, save_cached


async def run_full_analysis_cached(ticker: str) -> AnalysisResult:
    """Cached wrapper around run_full_analysis.

    Checks file cache first. On hit (within 24h, quality-gated),
    returns cached result instantly. On miss, runs full pipeline
    and persists result if quality gate passes (5+/8 agents OK).
    """
    cached = load_cached(ticker)
    if cached is not None:
        try:
            logger.info(f"📦 Cache HIT for {ticker} — returning instantly")
            return AnalysisResult(**cached)
        except Exception as e:
            logger.info(f"  Cache deserialize failed: {e} — running fresh")

    result = await run_full_analysis(ticker)
    save_cached(ticker, result)
    return result
