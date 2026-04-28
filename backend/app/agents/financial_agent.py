"""FinancialAgent — combines XBRL structured data with qualitative LLM analysis."""
from typing import Any

from app.agents.base_agent import BaseAgent
from app.services.llm_client import call_llm_json, MODEL_FLASH
from app.services.sec_edgar import get_filing_text
from app.services.xbrl_financials import fetch_structured_financials


SYSTEM_PROMPT = """You are a senior financial analyst at a top-tier private equity firm.
You extract qualitative insights from 10-K MD&A sections.
Be specific. Use the company's own language and numbers when discussing performance."""


USER_PROMPT_TEMPLATE = """Analyze this MD&A excerpt from {ticker}'s 10-K.
Return ONLY a JSON object with qualitative insights:

{{
  "key_drivers": [<3-5 specific revenue/profit drivers, e.g., "Services revenue grew 14% YoY">, ...],
  "key_risks": [<3-5 specific business risks, e.g., "Greater China revenue declined 8%">, ...],
  "non_recurring_items": [<one-time items affecting earnings, e.g., "$1.2B EU antitrust fine">, ...],
  "summary": "<2-3 sentence summary of the company's financial trajectory and PE attractiveness>"
}}

Use [] for any list field where you have nothing concrete. Never use null for lists.
Quote real numbers and segments mentioned in the filing.

MD&A excerpt:
---
{filing_text}
---"""


class FinancialAgent(BaseAgent):
    name = "financial_agent"

    async def run(self) -> dict[str, Any]:
        self.log("Extracting financials...")

        # Step 1: Pull structured numbers from SEC XBRL API (fast, accurate, no LLM)
        cik = self.filings.get("cik", "")
        structured = {}
        if cik:
            try:
                structured = fetch_structured_financials(cik)
            except Exception as e:
                self.log(f"XBRL fetch failed (will continue with LLM only): {e}")

        # Step 2: Run LLM on MD&A for qualitative analysis
        filing_obj = self.filings.get("_latest_10k_obj")
        qualitative = {
            "key_drivers": [],
            "key_risks": [],
            "non_recurring_items": [],
            "summary": "",
        }

        if filing_obj is not None:
            filing_text = get_filing_text(filing_obj, max_chars=35_000)
            if filing_text:
                self.log(f"Running qualitative LLM on {len(filing_text)} chars of MD&A...")
                prompt = USER_PROMPT_TEMPLATE.format(
                    ticker=self.ticker, filing_text=filing_text
                )
                try:
                    llm_data = await call_llm_json(
                        prompt=prompt, system=SYSTEM_PROMPT, model=MODEL_FLASH
                    )
                    qualitative = {
                        "key_drivers": llm_data.get("key_drivers") or [],
                        "key_risks": llm_data.get("key_risks") or [],
                        "non_recurring_items": llm_data.get("non_recurring_items") or [],
                        "summary": llm_data.get("summary") or "",
                    }
                except Exception as e:
                    self.log(f"Qualitative LLM call failed: {e}")

        # Step 3: Merge structured + qualitative
        merged = {**structured, **qualitative}

        # If revenue is present, compute YoY growth via second-most-recent year
        # (for now we leave revenue_growth_yoy_pct null unless XBRL gave it)

        self.log(
            f"Final: revenue=${merged.get('revenue_usd_millions')}M, "
            f"EBITDA=${merged.get('ebitda_usd_millions')}M, "
            f"FCF=${merged.get('free_cash_flow_usd_millions')}M, "
            f"drivers={len(merged.get('key_drivers', []))}, "
            f"risks={len(merged.get('key_risks', []))}"
        )

        return {"status": "ok", "data": merged}
