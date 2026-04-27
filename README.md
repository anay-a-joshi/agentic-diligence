# DiligenceAI

> Agentic AI Platform for Take-Private Screening — compresses PE due diligence from weeks to hours.

## Overview
DiligenceAI is a multi-agent system that analyzes any NYSE/NASDAQ-listed public company as a potential PE take-private target. It autonomously fetches SEC filings, runs LBO analysis, scores governance friendliness, and generates a partner-ready Investment Committee memo.

## Architecture
- **Frontend:** Next.js 14 + Tailwind + shadcn/ui
- **Backend:** FastAPI + LangGraph (multi-agent orchestration)
- **Data:** SEC EDGAR (free), yfinance for market data
- **LLM:** Anthropic Claude / OpenAI GPT-4
- **DB:** Supabase (Postgres + Storage)

## Quick Start
```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

## Project Structure
See `docs/architecture.md` for the full architecture writeup.

## Course
Final Project — NLP and GenAI in Finance, Georgia Tech QCF
