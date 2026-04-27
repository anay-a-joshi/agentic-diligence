"""MarketAgent — pulls market data, comps, and trading multiples."""
from typing import Any
from app.agents.base_agent import BaseAgent


class MarketAgent(BaseAgent):
    name = "market_agent"

    async def run(self) -> dict[str, Any]:
        self.log("Running analysis...")
        return {"status": "stub", "agent": self.name}
