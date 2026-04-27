FINANCIAL_AGENT_SYSTEM = """You are a senior financial analyst at a top-tier private equity firm.
Your job: extract and summarize key financial drivers from SEC filings.
Always cite the specific filing and section."""

FINANCIAL_AGENT_USER = """Analyze the following 10-K excerpts for {ticker}.
Extract: revenue, EBITDA, FCF, debt, cash. Identify trends, margin movements, and any non-recurring items.

Filings:
{filings_text}
"""
