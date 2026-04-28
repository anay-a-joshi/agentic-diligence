"""Base class for all specialist agents."""
from typing import Any
from app.utils.logger import logger


class BaseAgent:
    name: str = "base_agent"

    def __init__(self, ticker: str, filings: dict[str, Any]):
        self.ticker = ticker
        self.filings = filings

    def log(self, msg: str):
        logger.info(f"[{self.name}:{self.ticker}] {msg}")

    async def run(self) -> dict[str, Any]:
        raise NotImplementedError
