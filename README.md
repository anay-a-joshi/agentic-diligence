# DiligenceAI

> Agentic AI Platform for Take-Private Screening — compresses PE due diligence from weeks to hours.

## Overview
DiligenceAI is a multi-agent system that analyzes any NYSE/NASDAQ-listed public company as a potential PE take-private target. It autonomously fetches SEC filings, runs LBO analysis, scores governance friendliness, and generates a partner-ready Investment Committee memo.

## Architecture
- **Frontend:** Next.js 14 + Tailwind + shadcn/ui
- **Backend:** FastAPI + LangGraph (multi-agent orchestration)
- **Data:** SEC EDGAR (free), yfinance for market data
- **LLM:** Google Gemini (free tier)
- **DB:** Supabase (Postgres + Storage)

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- A free Gemini API key from https://aistudio.google.com/apikey

### Backend
```bash
cd backend
cp .env.example .env       # then add your GEMINI_API_KEY
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Open http://localhost:3000

## Project Structure
See `docs/architecture.md` for the full architecture writeup.

## Course
Final Project — NLP and GenAI in Finance, Georgia Tech QCF
