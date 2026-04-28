"""GovernanceAgent — assesses board, takeover defenses, ownership for take-private feasibility."""
from typing import Any

from app.agents.base_agent import BaseAgent
from app.services.llm_client import call_llm_json, MODEL_FLASH
from app.services.sec_edgar import get_proxy_text


SYSTEM_PROMPT = """You are a governance analyst at a private equity firm.
You read DEF 14A proxy statements and assess take-private feasibility — Board independence,
takeover defenses (poison pill, staggered board, supermajority), and ownership concentration."""


USER_PROMPT_TEMPLATE = """Analyze the proxy statement for {ticker} for take-private feasibility.

Return ONLY a JSON object:
{{
  "board_size": <int or null>,
  "independent_directors_pct": <number 0-100 or null>,
  "ceo_chair_combined": <true | false | null>,
  "staggered_board": <true | false | null>,
  "poison_pill": <true | false | null>,
  "supermajority_voting": <true | false | null>,
  "dual_class_shares": <true | false | null>,
  "insider_ownership_pct": <number or null>,
  "largest_holder": "<name and % if disclosed, else empty string>",
  "takeover_defense_strength": "<Low | Medium | High>",
  "feasibility_assessment": "<Easy | Moderate | Difficult>",
  "summary": "<2-3 sentences on take-private feasibility>"
}}

Be conservative — if not disclosed, use null. Use [] for empty lists.

Proxy excerpt:
---
{filing_text}
---"""


class GovernanceAgent(BaseAgent):
    name = "governance_agent"

    async def run(self) -> dict[str, Any]:
        self.log("Assessing governance & takeover defenses...")
        filing_obj = self.filings.get("_latest_def14a_obj")
        if filing_obj is None:
            self.log("No proxy available — returning empty result")
            return {"status": "no_filing", "data": None}

        text = get_proxy_text(filing_obj, max_chars=25_000)
        if not text:
            return {"status": "no_text", "data": None}

        prompt = USER_PROMPT_TEMPLATE.format(ticker=self.ticker, filing_text=text)
        try:
            data = await call_llm_json(prompt=prompt, system=SYSTEM_PROMPT, model=MODEL_FLASH)
            self.log(f"Feasibility: {data.get('feasibility_assessment')}, "
                     f"defense: {data.get('takeover_defense_strength')}")
            return {"status": "ok", "data": data}
        except Exception as e:
            self.log(f"LLM failed: {e}")
            return {"status": "error", "error": str(e), "data": None}
