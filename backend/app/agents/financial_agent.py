"""FinancialAgent — extracts financial drivers from SEC filings using Groq Llama."""
from typing import Any

from app.agents.base_agent import BaseAgent
from app.services.llm_client import call_llm_json, MODEL_FLASH
from app.services.sec_edgar import get_filing_text


SYSTEM_PROMPT = """You are a senior financial analyst at a top-tier private equity firm.
You read SEC 10-K filings and extract precise, structured financial data for LBO modeling.

CRITICAL RULES:
1. Extract every number you can find. Look for revenue, net sales, EBITDA, operating income,
   net income, cash flow from operations, capital expenditures, total debt, cash & equivalents.
2. Numbers in 10-Ks are usually stated in millions. Convert any thousands or billions accordingly.
3. If you find revenue but not EBITDA explicitly, calculate EBITDA = Operating Income + D&A
   when both are available.
4. Free Cash Flow = Cash from Operations - CapEx (when both are available).
5. ALWAYS return a list (possibly empty) for key_drivers, key_risks, non_recurring_items.
   Never return null for those fields - return [] if you have nothing.
6. Use null ONLY for numerical fields you genuinely cannot determine."""


USER_PROMPT_TEMPLATE = """This is the most recent 10-K filing for {ticker}. Extract financial data.

Return ONLY a JSON object:
{{
  "fiscal_year": <int>,
  "revenue_usd_millions": <number or null>,
  "ebitda_usd_millions": <number or null>,
  "net_income_usd_millions": <number or null>,
  "free_cash_flow_usd_millions": <number or null>,
  "total_debt_usd_millions": <number or null>,
  "cash_and_equivalents_usd_millions": <number or null>,
  "shares_outstanding_millions": <number or null>,
  "revenue_growth_yoy_pct": <number or null>,
  "ebitda_margin_pct": <number or null>,
  "key_drivers": [<string>, ...],
  "key_risks": [<string>, ...],
  "non_recurring_items": [<string>, ...],
  "summary": "<2-3 sentence summary>"
}}

For list fields, use [] if you have nothing — DO NOT use null.

10-K excerpt (focus on revenue, operating income, cash flow):
---
{filing_text}
---"""


class FinancialAgent(BaseAgent):
    name = "financial_agent"

    async def run(self) -> dict[str, Any]:
        self.log("Extracting financials from latest 10-K...")

        filing_obj = self.filings.get("_latest_10k_obj")
        if filing_obj is None:
            self.log("No 10-K available")
            return {"status": "no_filing", "data": None}

        filing_text = get_filing_text(filing_obj, max_chars=35_000)
        if not filing_text:
            self.log("Could not extract filing text")
            return {"status": "no_text", "data": None}

        self.log(f"Filing text: {len(filing_text)} chars")

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
            rev = data.get("revenue_usd_millions")
            ebitda = data.get("ebitda_usd_millions")
            self.log(f"Extracted: revenue=${rev}M, EBITDA=${ebitda}M")
            return {"status": "ok", "data": data}
        except Exception as e:
            self.log(f"LLM call failed: {e}")
            return {"status": "error", "error": str(e), "data": None}
