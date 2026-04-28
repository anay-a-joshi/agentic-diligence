"""RedFlagAgent — scans recent 8-Ks for material events that could derail an LBO."""
from typing import Any

from app.agents.base_agent import BaseAgent
from app.services.llm_client import call_llm_json, MODEL_FLASH
from app.services.sec_edgar import get_recent_8k_text


SYSTEM_PROMPT = """You are a forensic diligence analyst at a private equity firm.
You scan recent 8-K filings for ANY events that could derail a take-private deal:
executive departures, going concern disclosures, material lawsuits, restatements,
debt covenant violations, large losses, or activist investor positions."""


USER_PROMPT_TEMPLATE = """Scan {ticker}'s recent 8-K filings for red flags.

Return ONLY a JSON object:
{{
  "red_flags": [
    {{
      "flag": "<short title, e.g., 'CFO Resignation'>",
      "category": "<one of: Executive Departure, Material Litigation, Going Concern, Restatement, Debt Default, Large Loss, Activist Investor, Other>",
      "severity": "<Low | Medium | High | Critical>",
      "filing_date": "<approximate date if mentioned>",
      "description": "<1-2 sentence factual description from the filing>"
    }},
    ...
  ],
  "deal_breakers_count": <int — count of severity=Critical>,
  "high_concern_count": <int — count of severity=High>,
  "summary": "<2-3 sentences for an IC memo>"
}}

If no red flags found, return red_flags=[]. Quote real specific events, not generic concerns.

Recent 8-K filings:
---
{filing_text}
---"""


class RedFlagAgent(BaseAgent):
    name = "red_flag_agent"

    async def run(self) -> dict[str, Any]:
        self.log("Scanning 8-Ks for red flags...")
        filings_8k = self.filings.get("recent_8k_objs", [])
        if not filings_8k:
            return {"status": "no_filings", "data": {"red_flags": [], "summary": "No recent 8-Ks"}}

        text = get_recent_8k_text(filings_8k, max_chars=20_000)
        if not text:
            return {"status": "no_text", "data": None}

        prompt = USER_PROMPT_TEMPLATE.format(ticker=self.ticker, filing_text=text)
        try:
            data = await call_llm_json(prompt=prompt, system=SYSTEM_PROMPT, model=MODEL_FLASH)
            flags = data.get("red_flags") or []
            self.log(f"Found {len(flags)} red flags, "
                     f"{data.get('deal_breakers_count', 0)} critical, "
                     f"{data.get('high_concern_count', 0)} high")
            return {"status": "ok", "data": data}
        except Exception as e:
            self.log(f"LLM failed: {e}")
            return {"status": "error", "error": str(e), "data": None}
