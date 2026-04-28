"""CommercialAgent — analyzes business model, segments, customers, competition."""
from typing import Any

from app.agents.base_agent import BaseAgent
from app.services.llm_client import call_llm_json, MODEL_FLASH
from app.services.sec_edgar import get_business_section


SYSTEM_PROMPT = """You are a commercial diligence analyst at a private equity firm.
You read 10-K Item 1 (Business) sections and extract commercial insights for take-private screening."""


USER_PROMPT_TEMPLATE = """Analyze the Item 1 (Business) section of {ticker}'s 10-K.

Return ONLY a JSON object:
{{
  "business_segments": [<list of segment names with brief descriptions>],
  "primary_products": [<top 3-5 product/service lines>],
  "geographic_mix": "<short description of geographic revenue concentration>",
  "customer_concentration": "<None / Low / Medium / High — based on disclosed major customers>",
  "key_competitors": [<3-5 named competitors mentioned>],
  "competitive_advantages": [<3-5 specific moats: brand, scale, IP, network effects, etc.>],
  "growth_strategy": "<2-3 sentence summary of how the company plans to grow>",
  "summary": "<2-3 sentence commercial assessment for a PE buyer>"
}}

Use [] for any list field with nothing concrete. NEVER use null for lists.

Item 1 (Business) excerpt:
---
{filing_text}
---"""


class CommercialAgent(BaseAgent):
    name = "commercial_agent"

    async def run(self) -> dict[str, Any]:
        self.log("Analyzing business model & competitive position...")
        filing_obj = self.filings.get("_latest_10k_obj")
        if filing_obj is None:
            return {"status": "no_filing", "data": None}

        text = get_business_section(filing_obj, max_chars=25_000)
        if not text:
            return {"status": "no_text", "data": None}

        prompt = USER_PROMPT_TEMPLATE.format(ticker=self.ticker, filing_text=text)
        try:
            data = await call_llm_json(prompt=prompt, system=SYSTEM_PROMPT, model=MODEL_FLASH)
            self.log(f"Segments: {len(data.get('business_segments', []))}, "
                     f"competitors: {len(data.get('key_competitors', []))}")
            return {"status": "ok", "data": data}
        except Exception as e:
            self.log(f"LLM failed: {e}")
            return {"status": "error", "error": str(e), "data": None}
