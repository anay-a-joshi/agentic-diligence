"""SynthesisAgent — combines outputs into IC memo executive summary.

Has a deterministic fallback when LLM is unavailable, so the pipeline
still produces a usable IC memo even when rate-limited.
"""
from typing import Any
import json

from app.agents.base_agent import BaseAgent
from app.services.llm_client import call_llm_json, MODEL_FLASH


SYSTEM_PROMPT = """You are a senior partner at a top-tier private equity firm writing an
Investment Committee (IC) memo for a take-private candidate. You synthesize findings from
multiple diligence workstreams into a sharp, decision-ready recommendation.
Your tone is direct, quantitative, and skeptical."""


USER_PROMPT_TEMPLATE = """Write the IC memo executive summary for {ticker} ({company_name}).

INPUTS (already-completed diligence findings):
{findings_json}

LBO RETURNS:
{lbo_summary_json}

FEASIBILITY SCORE: {score}/100 (Grade {grade}) — {verdict}

Produce ONLY a JSON object:
{{
  "executive_summary": "<3-4 sentence one-paragraph thesis>",
  "investment_thesis": [<3-4 specific, quantitative bullet points>],
  "key_risks_to_thesis": [<3-4 specific bullet points>],
  "value_creation_levers": [<3-4 specific operational/strategic levers>],
  "recommendation": "<one of: PROCEED TO IC | PROCEED WITH CAVEATS | PASS>",
  "recommendation_rationale": "<2-3 sentence rationale>",
  "next_steps": [<3-4 concrete next-step actions>]
}}

Be specific — quote real numbers and findings. Use [] for empty lists, never null."""


def _make_fallback_synthesis(
    ticker: str,
    company_name: str,
    financial: dict,
    market: dict,
    feasibility: dict,
    lbo_summary: dict,
) -> dict:
    """Deterministic synthesis when LLM is rate-limited.

    Builds a serviceable executive summary purely from numeric inputs.
    """
    rev = financial.get("revenue_usd_millions")
    ebitda = financial.get("ebitda_usd_millions")
    margin = financial.get("ebitda_margin_pct")
    fcf = financial.get("free_cash_flow_usd_millions")
    growth = financial.get("revenue_growth_yoy_pct")
    mkt_cap = market.get("market_cap_usd_millions")
    pe = market.get("pe_ratio")

    score = feasibility.get("score", 0)
    grade = feasibility.get("grade", "?")
    verdict = feasibility.get("verdict", "")
    base_irr = lbo_summary.get("irr_base_pct", 0)
    base_moic = lbo_summary.get("moic_base", 0)

    rec = "PASS"
    if score >= 70: rec = "PROCEED TO IC"
    elif score >= 60: rec = "PROCEED WITH CAVEATS"

    def fmt_money(v):
        if v is None: return "n/a"
        if abs(v) >= 1000: return f"${v/1000:.1f}B"
        return f"${v:,.0f}M"

    exec_summary = (
        f"{company_name} ({ticker}) generates {fmt_money(rev)} of revenue with "
        f"{margin:.1f}% EBITDA margins" if margin is not None else
        f"{company_name} ({ticker}) generates {fmt_money(rev)} of revenue"
    )
    exec_summary += (
        f" and {fmt_money(fcf)} of FCF. " if fcf is not None else ". "
    )
    exec_summary += (
        f"Current market cap of {fmt_money(mkt_cap)} at {pe:.1f}x P/E. "
        if pe is not None else ""
    )
    exec_summary += (
        f"Base-case LBO yields {base_irr:.1f}% IRR / {base_moic:.2f}x MOIC over a 5-year hold. "
        f"Composite feasibility score: {score}/100 (Grade {grade}) — {verdict}."
    )

    thesis = []
    if margin is not None and margin >= 25:
        thesis.append(f"Strong cash generation: {margin:.1f}% EBITDA margins — well above PE LBO threshold")
    if fcf is not None and rev:
        fcf_conv = fcf / rev * 100
        thesis.append(f"FCF conversion of {fcf_conv:.1f}% supports debt service through hold period")
    if base_irr >= 15:
        thesis.append(f"Modeled base-case IRR of {base_irr:.1f}% clears typical PE hurdle rate")
    if growth is not None:
        if growth > 0:
            thesis.append(f"Revenue growth of {growth:.1f}% YoY provides organic top-line tailwind")
        else:
            thesis.append(f"Revenue declined {abs(growth):.1f}% YoY — turnaround/cost-out thesis required")

    risks_to_thesis = []
    risks_to_thesis.append("Multiple compression risk if exit environment deteriorates")
    if pe is not None and pe > 25:
        risks_to_thesis.append(f"Elevated entry multiple at {pe:.1f}x P/E limits upside; bull case requires multiple expansion")
    risks_to_thesis.append("Interest rate sensitivity: ~55% leverage at close compounds rate-shock impact on returns")
    if mkt_cap and mkt_cap > 100_000:
        risks_to_thesis.append(f"Sheer size ({fmt_money(mkt_cap)}) may exceed even mega-fund check-size capacity")

    levers = [
        "Operational efficiency / G&A rationalization (typical 2-4% margin expansion in PE-owned mode)",
        "Pricing optimization across product portfolio",
        "Working capital optimization — inventory & receivables tightening",
        "Strategic add-on M&A to consolidate fragmented adjacencies",
    ]

    rec_rationale = (
        f"Score of {score}/100 places this candidate in the '{verdict}' band. "
        f"Base-case modeled returns of {base_irr:.1f}% IRR are "
        + ("compelling. " if base_irr >= 20 else
           "adequate. " if base_irr >= 15 else
           "below typical PE hurdle. ")
        + "Recommendation: " + rec + "."
    )

    next_steps = [
        "Commission management presentation and Q&A session",
        "Deeper financial diligence on segment-level economics and quality of earnings",
        "Engage legal counsel on takeover-defense analysis and regulatory clearance",
        "Build full operating model with detailed cost structure and unit economics",
    ]

    return {
        "executive_summary": exec_summary,
        "investment_thesis": thesis,
        "key_risks_to_thesis": risks_to_thesis,
        "value_creation_levers": levers,
        "recommendation": rec,
        "recommendation_rationale": rec_rationale,
        "next_steps": next_steps,
        "_fallback_used": True,
    }


class SynthesisAgent(BaseAgent):
    name = "synthesis_agent"

    def __init__(self, ticker: str, filings: dict, all_findings: dict,
                 lbo_summary: dict, feasibility: dict, company_name: str,
                 financial: dict | None = None, market: dict | None = None):
        super().__init__(ticker=ticker, filings=filings)
        self.all_findings = all_findings
        self.lbo_summary = lbo_summary
        self.feasibility = feasibility
        self.company_name = company_name
        self.financial = financial or {}
        self.market = market or {}

    async def run(self) -> dict[str, Any]:
        self.log("Synthesizing IC memo executive summary...")

        compact: dict[str, Any] = {}
        for k, v in self.all_findings.items():
            if isinstance(v, dict) and v.get("status") == "ok":
                compact[k] = v.get("data", {})

        findings_json = json.dumps(compact, indent=2)[:12_000]
        lbo_json = json.dumps(self.lbo_summary, indent=2)[:2_000]

        prompt = USER_PROMPT_TEMPLATE.format(
            ticker=self.ticker, company_name=self.company_name,
            findings_json=findings_json, lbo_summary_json=lbo_json,
            score=self.feasibility.get("score"),
            grade=self.feasibility.get("grade"),
            verdict=self.feasibility.get("verdict"),
        )

        try:
            data = await call_llm_json(prompt=prompt, system=SYSTEM_PROMPT, model=MODEL_FLASH)
            self.log(f"Recommendation: {data.get('recommendation')}")
            return {"status": "ok", "data": data}
        except Exception as e:
            self.log(f"Synthesis LLM failed (using deterministic fallback): {e}")
            fallback = _make_fallback_synthesis(
                ticker=self.ticker, company_name=self.company_name,
                financial=self.financial, market=self.market,
                feasibility=self.feasibility, lbo_summary=self.lbo_summary,
            )
            return {"status": "ok_fallback", "data": fallback}
