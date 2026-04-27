# Agent Design

| Agent | Input | Output | Tools |
|---|---|---|---|
| Financial | 10-K, 10-Q | Revenue, EBITDA, FCF trends | LLM, pandas |
| Commercial | MD&A, segment data | Segment growth, customer concentration | LLM |
| Risk | Risk Factors, 8-K | Categorized risks | LLM |
| Governance | DEF 14A | Friendliness score, anti-takeover provisions | LLM |
| Market | Market data, comps | Trading multiples, peer set | LLM, yfinance |
| Sentiment | Earnings transcripts | Tone shifts over time | LLM |
| Red Flag | All above | Cross-cutting inconsistencies | LLM |
| Synthesis | All above | Final IC memo + score | LLM |
