"""Pre-fetches and caches analyses for demo tickers (so cold-start is instant)."""
import asyncio

DEMO_TICKERS = ["DOCN", "AAPL", "MSFT"]


async def main():
    for ticker in DEMO_TICKERS:
        print(f"Seeding {ticker}...")
        # TODO: call run_full_analysis and persist to Supabase
    print("✅ Done")


if __name__ == "__main__":
    asyncio.run(main())
