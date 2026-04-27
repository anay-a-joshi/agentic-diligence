"""Base class for all specialist agents."""
from abc import ABC, abstractmethod
from typing import Any

from app.utils.logger import logger


class BaseAgent(ABC):
    name: str = "base"

    def __init__(self, ticker: str, filings: dict[str, Any]):
        self.ticker = ticker
        self.filings = filings

    @abstractmethod
    async def run(self) -> dict[str, Any]:
        """Execute the agent's analysis. Must return a dict of findings."""
        ...

    def log(self, msg: str):
        logger.info(f"[{self.name}:{self.ticker}] {msg}")
