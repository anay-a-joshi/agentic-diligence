"""RiskAgent — extracts and ranks risks from 10-K Risk Factors section."""
from typing import Any

from app.agents.base_agent import BaseAgent
from app.services.llm_client import call_llm_json, MODEL_FLASH
from app.services.sec_edgar import get_risk_factors


SYSTEM_PROMPT = """You are a risk diligence analyst at a private equity firm.
You read 10-K Item 1A (Risk Factors) sections and rank the most material risks for an LBO."""


USER_PROMPT_TEMPLATE = """Read {ticker}'s Risk Factors and identify the most material LBO risks.

Return ONLY a JSON object:
{{
  "top_risks": [
    {{
      "risk": "<short title>",
      "category": "<one of: Macro, Operational, Regulatory, Litigation, Cyber, Concentration, Financial>",
      "severity": "<Low | Medium | High>",
      "description": "<1-2 sentence specific description from the filing>"
    }},
    ...
  ],
  "total_risks_disclosed": <int>,
  "high_severity_count": <int>,
  "summary": "<2-3 sentence risk assessment for a PE buyer>"
}}

List exactly 5 top_risks ranked by materiality. Use specific risks from the filing — not generic text.

Risk Factors excerpt:
---
{filing_text}
---"""


class RiskAgent(BaseAgent):
    name = "risk_agent"

    async def run(self) -> dict[str, Any]:
        self.log("Analyzing risk factors...")
        filing_obj = self.filings.get("_latest_10k_obj")
        if filing_obj is None:
            return {"status": "no_filing", "data": None}

        text = get_risk_factors(filing_obj, max_chars=25_000)
        if not text:
            return {"status": "no_text", "data": None}

        prompt = USER_PROMPT_TEMPLATE.format(ticker=self.ticker, filing_text=text)
        try:
            data = await call_llm_json(prompt=prompt, system=SYSTEM_PROMPT, model=MODEL_FLASH)
            risks = data.get("top_risks") or []
            high_count = sum(1 for r in risks if str(r.get("severity", "")).lower() == "high")
            self.log(f"Identified {len(risks)} top risks, {high_count} high-severity")
            return {"status": "ok", "data": data}
        except Exception as e:
            self.log(f"LLM failed: {e}")
            return {"status": "error", "error": str(e), "data": None}
