"""SentimentAgent — analyzes management tone & hedging language."""
from typing import Any

from app.agents.base_agent import BaseAgent
from app.services.llm_client import call_llm_json, MODEL_FLASH
from app.services.sec_edgar import get_filing_text


SYSTEM_PROMPT = """You are a forensic analyst at a private equity firm.
You read MD&A sections and detect management tone shifts, hedging language, and uncertainty signals.
You are skeptical and look for what management is NOT saying clearly."""


USER_PROMPT_TEMPLATE = """Analyze management's tone in {ticker}'s MD&A.

Return ONLY a JSON object:
{{
  "overall_tone": "<Confident | Cautious | Defensive | Mixed>",
  "uncertainty_phrases": [<2-5 hedging phrases verbatim, e.g., "may be adversely affected">],
  "tone_red_flags": [<2-5 specific phrases that suggest concern, e.g., "headwinds intensified">],
  "tone_positive_signals": [<2-5 confident statements>],
  "yoy_tone_shift": "<More positive | More negative | Similar | Unclear>",
  "summary": "<2-3 sentence assessment of management's confidence level>"
}}

Use [] for empty lists. Be specific — quote actual filing language.

MD&A excerpt:
---
{filing_text}
---"""


class SentimentAgent(BaseAgent):
    name = "sentiment_agent"

    async def run(self) -> dict[str, Any]:
        self.log("Analyzing management tone...")
        filing_obj = self.filings.get("_latest_10k_obj")
        if filing_obj is None:
            return {"status": "no_filing", "data": None}

        text = get_filing_text(filing_obj, max_chars=25_000)
        if not text:
            return {"status": "no_text", "data": None}

        prompt = USER_PROMPT_TEMPLATE.format(ticker=self.ticker, filing_text=text)
        try:
            data = await call_llm_json(prompt=prompt, system=SYSTEM_PROMPT, model=MODEL_FLASH)
            self.log(f"Tone: {data.get('overall_tone')}, shift: {data.get('yoy_tone_shift')}")
            return {"status": "ok", "data": data}
        except Exception as e:
            self.log(f"LLM failed: {e}")
            return {"status": "error", "error": str(e), "data": None}
