"""MarketAgent — pulls trading data and computes premium-to-buy estimates. No LLM needed."""
from typing import Any

from app.agents.base_agent import BaseAgent
from app.services.market_data import fetch_market_data


class MarketAgent(BaseAgent):
    name = "market_agent"

    async def run(self) -> dict[str, Any]:
        self.log("Pulling market data...")
        data = fetch_market_data(self.ticker)
        if not data:
            return {"status": "no_data", "data": None}

        # Compute typical PE take-private premium estimate (30-40% over current)
        price = data.get("current_price")
        if price:
            data["estimated_take_private_price_low"] = round(price * 1.30, 2)
            data["estimated_take_private_price_high"] = round(price * 1.40, 2)

        # Estimate take-private equity check at midpoint
        mkt_cap = data.get("market_cap_usd_millions")
        if mkt_cap:
            data["estimated_equity_check_usd_millions"] = round(mkt_cap * 1.35)

        return {"status": "ok", "data": data}
