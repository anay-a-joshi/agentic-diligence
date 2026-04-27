"""FinancialAgent — extracts financial drivers from SEC filings using Groq Llama."""
from typing import Any

from app.agents.base_agent import BaseAgent
from app.services.llm_client import call_llm_json, MODEL_FLASH
from app.services.sec_edgar import get_filing_text


SYSTEM_PROMPT = """You are a senior financial analyst at a top-tier private equity firm.
You read SEC 10-K filings and extract clean, structured financial data for use in LBO modeling.
You are precise. You only return what is explicitly stated in the filing.
If a value is unclear or not stated, return null for that field rather than guessing."""


USER_PROMPT_TEMPLATE = """Analyze the following 10-K filing for {ticker} and extract the most recent fiscal year's key financial data.

Return ONLY a JSON object with this exact shape:
{{
  "fiscal_year": 2024,
  "revenue_usd_millions": 391035,
  "ebitda_usd_millions": 130000,
  "net_income_usd_millions": 96995,
  "free_cash_flow_usd_millions": 108807,
  "total_debt_usd_millions": 106629,
  "cash_and_equivalents_usd_millions": 65171,
  "shares_outstanding_millions": 15116,
  "revenue_growth_yoy_pct": 2.0,
  "ebitda_margin_pct": 33.2,
  "key_drivers": ["Services revenue growth", "iPhone unit pricing"],
  "key_risks": ["China demand softness", "Regulatory pressure on App Store"],
  "non_recurring_items": ["1.2B litigation reserve in Q3"],
  "summary": "A 2-3 sentence summary of financial health and trajectory."
}}

Use null for any value you cannot determine. Numbers in USD millions.

10-K excerpt:
---
{filing_text}
---"""


class FinancialAgent(BaseAgent):
    name = "financial_agent"

    async def run(self) -> dict[str, Any]:
        self.log("Extracting financials from latest 10-K...")

        filing_obj = self.filings.get("_latest_10k_obj")
        if filing_obj is None:
            self.log("No 10-K available — returning empty result")
            return {"status": "no_filing", "data": None}

        # Groq has a 128K context limit; truncate to 70K chars to leave room for prompt + response
        filing_text = get_filing_text(filing_obj, max_chars=70_000)
        if not filing_text:
            self.log("Could not extract filing text")
            return {"status": "no_text", "data": None}

        prompt = USER_PROMPT_TEMPLATE.format(
            ticker=self.ticker,
            filing_text=filing_text,
        )

        try:
            data = await call_llm_json(
                prompt=prompt,
                system=SYSTEM_PROMPT,
                model=MODEL_FLASH,
            )
            self.log(f"Extracted: revenue=${data.get('revenue_usd_millions')}M, "
                     f"EBITDA=${data.get('ebitda_usd_millions')}M")
            return {"status": "ok", "data": data}
        except Exception as e:
            self.log(f"LLM call failed: {e}")
            return {"status": "error", "error": str(e), "data": None}
