"""FinancialAgent — extracts financial drivers from filings."""
from typing import Any
from app.agents.base_agent import BaseAgent


class FinancialAgent(BaseAgent):
    name = "financial_agent"

    async def run(self) -> dict[str, Any]:
        self.log("Running analysis...")
        return {"status": "stub", "agent": self.name}
