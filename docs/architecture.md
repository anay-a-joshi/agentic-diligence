# DiligenceAI — System Architecture

## Overview
DiligenceAI is a multi-agent system for screening public companies as PE take-private targets.

## Components
1. **Frontend (Next.js)** — ticker input, dashboard, chatbot
2. **Backend (FastAPI)** — orchestrator API
3. **Agent Layer (LangGraph)** — 8 specialized agents
4. **Data Layer** — SEC EDGAR + yfinance + Supabase cache
5. **Generation Layer** — PDF (ReportLab) + Excel (openpyxl)

## Data Flow
1. User enters ticker → frontend calls `/analyze/{ticker}`
2. Backend fetches 5 years of filings from SEC EDGAR
3. Orchestrator dispatches Financial / Commercial / Risk / Governance / Market / Sentiment agents in parallel
4. Red Flag Agent cross-checks outputs for inconsistencies
5. Synthesis Agent produces IC memo + feasibility score
6. Generators build PDF + Excel artifacts
7. Frontend renders dashboard + provides downloads
