# HELIOS

> **Agentic AI for Private Equity Take-Private Diligence — compresses 4-8 weeks of analyst work into ~2 minutes.**

[![Stack](https://img.shields.io/badge/stack-FastAPI%20%7C%20Next.js%2015-06B6D4)]()
[![LLM](https://img.shields.io/badge/LLM-Llama%203.3%2070B%20via%20Groq-8B5CF6)]()
[![License](https://img.shields.io/badge/license-Academic-10B981)]()

HELIOS is a multi-agent AI platform that takes any public US company ticker, autonomously reads its SEC filings, runs a five-year LBO model with Bull/Base/Bear scenarios, scores it across six dimensions, and produces a partner-ready Investment Committee memo plus a live editable Excel model — all in approximately two minutes.

> Final project for **MGT-8803-SC: NLP and Generative AI in Finance**, Scheller College of Business, Georgia Institute of Technology. Faculty: Professor Sudheer Chava.

---

## Why HELIOS

A typical PE take-private screen takes a junior associate four to eight weeks and costs $300K-$800K in labor. Roughly 95% of screened candidates never become deals. HELIOS automates the screening layer end-to-end, so analysts can focus on the 5% that matter.

| Dimension | Manual Screening | HELIOS |
|---|---|---|
| Time per candidate | 4-8 weeks | ~2 minutes |
| Cost per screen | $300K-$800K | < $1 in compute |
| Deliverables | Slides built by hand | PDF memo + live Excel model |
| Reproducibility | Weak; ad-hoc | Versioned, cached, audit-trailed |

---

## Eight-Agent Architecture

HELIOS orchestrates eight specialist agents. Seven extract structured insights from filings and market data; the eighth synthesizes them into a final memo.

| # | Agent | Source | Output |
|---|---|---|---|
| 1 | **Financial** | XBRL companyfacts + 10-K MD&A | Revenue, EBITDA, FCF, debt, drivers, risks |
| 2 | **Commercial** | 10-K Item 1 (Business) | Segments, products, named competitors |
| 3 | **Risk** | 10-K Item 1A (Risk Factors) | Top five risks ranked by severity |
| 4 | **Governance** | DEF 14A proxy statements | Board, takeover defenses, ownership |
| 5 | **Market** | yfinance | Live price, market cap, P/E, beta |
| 6 | **Sentiment** | 10-K MD&A | Management tone + YoY directional shift |
| 7 | **Red Flag** | Recent 8-K filings | Material adverse events |
| 8 | **Synthesis** | All seven above | IC memo executive summary + thesis |

Pure-Python deterministic modules sit alongside the agents:

- **LBO Engine** — five-year projections (Base / Bull / Bear), compounding revenue, FCF-driven debt paydown, exit multiple, IRR, MOIC.
- **Feasibility Scoring** — composite score 0-100 across six weighted dimensions, mapped to PE recommendations (Pursue / Conditional / Pass).
- **Sensitivity** — 5×5 IRR heatmap by Exit Multiple × Revenue Growth.

---

## Deliverables Generated Per Run

1. **0-100 Feasibility Score** with weighted breakdown across six dimensions
2. **3-page IC Memo (PDF)** — executive summary, thesis, value-creation levers, risks, score breakdown, next steps
3. **Live LBO Excel Model** — six tabs (Summary, Base, Bull, Bear, Sensitivity, Inputs Reference) with **real Excel formulas**, not pre-computed values. Editing any blue input cell triggers full recalculation.
4. **Premium Web Dashboard** — score gauge, headline metrics, LBO scenario cards, projection chart, downloadable artifacts.

---

## Tech Stack

**Backend** — FastAPI · Python 3.11 · Llama 3.3 70B via Groq · edgartools (SEC EDGAR) · yfinance · ReportLab (PDF) · openpyxl (Excel) · file-based result cache (24h TTL)

**Frontend** — Next.js 15 · React 19 · TypeScript · Tailwind v3.4 · Recharts · custom dark glassmorphism UI

**Data** — SEC EDGAR XBRL companyfacts API · 10-K, 10-Q, 8-K, DEF 14A filings · yfinance for live market data

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- A Groq API key (free tier available at https://console.groq.com)

### Backend
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # add GROQ_API_KEY and SEC_USER_AGENT
uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:3000

### Try It
Open http://localhost:3000 and click any ticker chip (DELL, HUBB, NCR) or enter your own. First-time analysis runs the full eight-agent pipeline in ~60-120 seconds; subsequent loads hit the 24-hour cache and return in under a second.

---

## Validated Example: Dell Technologies (DELL)

End-to-end run on a real take-private candidate:

| Metric | Value |
|---|---|
| Revenue (FY2026) | $88.4B |
| EBITDA | $8.7B (9.9% margin) |
| Free Cash Flow | $5.9B |
| Market Cap | $140.4B |
| Enterprise Value | $160.2B |
| Base Case IRR / MOIC | -14.6% / 0.45x |
| Bull Case IRR / MOIC | +10.3% / 1.63x |
| Bear Case IRR / MOIC | +1.8% / 1.09x |
| Composite Score | **40 / 100 (Grade F)** |
| Recommendation | **PASS — Fundamental Issues** |

The system correctly flags Dell as size-prohibitive: an $83.7B equity check exceeds the practical $50B PE LBO ceiling that even mega-funds operate within. This demonstrates the model's economic intelligence, not just data extraction.

---

## Project Structure

```
diligence-ai/
├── backend/
│   ├── app/
│   │   ├── agents/              # 8 specialist agents + orchestrator
│   │   ├── services/            # LBO engine, scoring, SEC, market data, cache
│   │   ├── generators/          # PDF and Excel deliverable builders
│   │   ├── api/routes/          # FastAPI endpoints
│   │   └── models/              # Pydantic schemas
│   ├── cache/                   # 24h result cache (gitignored)
│   ├── generated_outputs/       # PDFs and Excels (gitignored)
│   └── scripts/precache_demo.sh # Pre-warm cache for demos
├── frontend/
│   ├── app/                     # Next.js 15 app router
│   └── components/              # Premium dark UI components
└── HELIOS_Presentation.pptx     # Final project deck
```

---

## Disclaimer

HELIOS is an academic prototype. Outputs are not investment advice. All financial data is sourced from public SEC filings and market data feeds. Use of this software is governed by the academic license terms of the course.

![Profile Views](https://komarev.com/ghpvc/?username=anay-a-joshi&color=06B6D4)
