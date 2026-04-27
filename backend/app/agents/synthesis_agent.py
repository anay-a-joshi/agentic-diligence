"""Synthesizes all agent outputs into final IC memo + feasibility score."""
from typing import Any
from app.agents.base_agent import BaseAgent


class SynthesisAgent(BaseAgent):
    name = "synthesis_agent"

    async def run(self) -> dict[str, Any]:
        return {}

    async def synthesize(
        self, findings: dict[str, Any], red_flags: list[str]
    ) -> dict[str, Any]:
        self.log("Synthesizing IC memo...")
        # TODO: generate IC memo + feasibility score via LLM
        return {
            "ticker": self.ticker,
            "company_name": "TODO",
            "feasibility_score": 0,
            "lbo_irr_base": 0.0,
            "lbo_irr_bull": 0.0,
            "lbo_irr_bear": 0.0,
            "red_flags": red_flags,
            "ic_memo_url": "",
            "lbo_excel_url": "",
        }
