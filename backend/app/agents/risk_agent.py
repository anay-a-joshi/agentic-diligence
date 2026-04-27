"""RiskAgent — parses Risk Factors and recent material events."""
from typing import Any
from app.agents.base_agent import BaseAgent


class RiskAgent(BaseAgent):
    name = "risk_agent"

    async def run(self) -> dict[str, Any]:
        self.log("Running analysis...")
        return {"status": "stub", "agent": self.name}
