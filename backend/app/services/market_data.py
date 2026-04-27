"""Stock prices, betas, market caps via yfinance."""
import yfinance as yf


def get_market_data(ticker: str) -> dict:
    t = yf.Ticker(ticker)
    info = t.info
    hist = t.history(period="2y")
    return {
        "current_price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "beta": info.get("beta"),
        "history": hist.to_dict(),
    }
