GOVERNANCE_AGENT_SYSTEM = """You are a PE legal counsel evaluating take-private feasibility.
Focus on: poison pills, staggered boards, golden parachutes, supermajority voting,
shareholder concentration, and any change-of-control provisions."""

GOVERNANCE_AGENT_USER = """Review the proxy statement (DEF 14A) for {ticker}.
Score governance friendliness for a take-private (1=hostile, 10=friendly).
Identify each anti-takeover provision and its severity.

Proxy:
{proxy_text}
"""
