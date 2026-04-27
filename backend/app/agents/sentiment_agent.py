"""SentimentAgent — analyzes management tone shifts across earnings calls."""
from typing import Any
from app.agents.base_agent import BaseAgent


class SentimentAgent(BaseAgent):
    name = "sentiment_agent"

    async def run(self) -> dict[str, Any]:
        self.log("Running analysis...")
        return {"status": "stub", "agent": self.name}
