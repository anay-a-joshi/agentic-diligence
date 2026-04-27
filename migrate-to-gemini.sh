#!/bin/bash
# ============================================================
# DiligenceAI - Migrate from Anthropic to Google Gemini
# Run this from inside the diligence-ai/ project root
# Usage: bash migrate-to-gemini.sh
# ============================================================

set -e

# Verify we're in the right place
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
  echo "❌ Error: Run this script from the diligence-ai/ project root."
  echo "   cd ~/Downloads/diligence-ai && bash migrate-to-gemini.sh"
  exit 1
fi

echo "🔄 Migrating DiligenceAI from Anthropic to Google Gemini..."

# ============================================================
# 1. Update requirements.txt — swap anthropic for google-genai
# ============================================================
echo "📦 Updating backend/requirements.txt..."

cat > backend/requirements.txt << 'EOF'
fastapi==0.115.0
uvicorn[standard]==0.30.6
pydantic==2.9.0
pydantic-settings==2.5.2
python-dotenv==1.0.1
httpx==0.27.2

# AI / Agents
google-genai==0.3.0
langgraph==0.2.34
langchain==0.3.3
langchain-google-genai==2.0.1

# SEC + Market data
edgartools==2.7.0
yfinance==0.2.43

# Data / Math
pandas==2.2.3
numpy==2.1.1
scipy==1.14.1

# File generation
openpyxl==3.1.5
reportlab==4.2.2
jinja2==3.1.4

# DB
supabase==2.8.1

# Utils
tenacity==9.0.0
python-multipart==0.0.10
EOF

# ============================================================
# 2. Update .env.example
# ============================================================
echo "📝 Updating backend/.env.example..."

cat > backend/.env.example << 'EOF'
# LLM API Keys
GEMINI_API_KEY=AIza...

# SEC (edgartools works free, no key needed)
SEC_USER_AGENT="DiligenceAI Research yourname@gatech.edu"

# Supabase (optional - for caching, fill in when deploying)
SUPABASE_URL=
SUPABASE_KEY=

# App
APP_ENV=development
LOG_LEVEL=INFO
ALLOWED_ORIGINS=http://localhost:3000
EOF

# ============================================================
# 3. Update config.py — swap api key fields
# ============================================================
echo "⚙️  Updating backend/app/config.py..."

cat > backend/app/config.py << 'EOF'
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # LLM
    gemini_api_key: str = ""

    # SEC
    sec_user_agent: str = "DiligenceAI Research contact@example.com"

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""

    # App
    app_env: str = "development"
    log_level: str = "INFO"
    allowed_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
EOF

# ============================================================
# 4. Rewrite llm_client.py for Gemini
# ============================================================
echo "🤖 Rewriting backend/app/services/llm_client.py..."

cat > backend/app/services/llm_client.py << 'EOF'
"""Wraps Google Gemini client with retry + telemetry."""
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings
from app.utils.logger import logger


# Gemini model tiers — Flash is fast/free, Pro is higher quality
MODEL_FLASH = "gemini-2.0-flash-exp"   # use for cheap, fast agent calls
MODEL_PRO = "gemini-1.5-pro"           # use for synthesis & long-context work


_client: genai.Client | None = None


def get_client() -> genai.Client:
    """Lazy singleton — created on first use so missing keys don't crash startup."""
    global _client
    if _client is None:
        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to backend/.env"
            )
        _client = genai.Client(api_key=settings.gemini_api_key)
    return _client


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True,
)
async def call_llm(
    prompt: str,
    system: str = "",
    model: str = MODEL_FLASH,
    max_tokens: int = 4096,
    temperature: float = 0.2,
) -> str:
    """
    Send a prompt to Gemini and return the text response.

    Args:
        prompt: User-facing prompt content
        system: System instruction (optional)
        model: Gemini model identifier — defaults to fast/free Flash
        max_tokens: Output cap
        temperature: 0.0 = deterministic, 1.0 = creative
    """
    client = get_client()

    config = types.GenerateContentConfig(
        max_output_tokens=max_tokens,
        temperature=temperature,
    )
    if system:
        config.system_instruction = system

    try:
        response = await client.aio.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
        return response.text or ""
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise


async def call_llm_json(prompt: str, system: str = "", model: str = MODEL_FLASH) -> dict:
    """Convenience wrapper that asks Gemini to return JSON and parses it."""
    import json

    full_prompt = (
        f"{prompt}\n\n"
        "Respond with ONLY a valid JSON object. "
        "No markdown fences, no preamble, no explanation."
    )
    raw = await call_llm(full_prompt, system=system, model=model, temperature=0.0)
    # Strip code fences if the model included them anyway
    cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(cleaned)
EOF

# ============================================================
# 5. Update prompts to reference Gemini-friendly conventions
# ============================================================
echo "💬 Updating prompts/__init__.py with Gemini model constants..."

cat > backend/app/prompts/__init__.py << 'EOF'
"""Centralized prompts for all agents."""
from app.services.llm_client import MODEL_FLASH, MODEL_PRO

# Use Flash for per-agent fast calls; Pro for synthesis where quality matters most
AGENT_MODEL = MODEL_FLASH
SYNTHESIS_MODEL = MODEL_PRO
EOF

# ============================================================
# 6. Update README with the new env var
# ============================================================
echo "📖 Updating README.md..."

cat > README.md << 'EOF'
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
EOF

# ============================================================
# 7. Migrate user's existing .env if it exists
# ============================================================
if [ -f "backend/.env" ]; then
  echo "🔑 Found existing backend/.env — checking for API keys..."

  if grep -q "^GEMINI_API_KEY=" backend/.env && ! grep -q "^GEMINI_API_KEY=AIza\.\.\.$" backend/.env; then
    echo "   ✅ GEMINI_API_KEY already present in .env — keeping it"
  else
    echo ""
    echo "   ⚠️  Your backend/.env doesn't have a GEMINI_API_KEY yet."
    echo ""
    read -p "   Paste your Gemini API key now (starts with AIza...): " GEMINI_KEY

    if [ -z "$GEMINI_KEY" ]; then
      echo "   ⏭️  Skipped. Edit backend/.env manually before running the backend."
      cp backend/.env.example backend/.env.new
      mv backend/.env.new backend/.env
    else
      # Build a fresh .env from the example, with the user's key inserted
      sed "s|GEMINI_API_KEY=AIza\.\.\.|GEMINI_API_KEY=$GEMINI_KEY|" backend/.env.example > backend/.env
      echo "   ✅ Wrote new backend/.env with your Gemini key"
    fi
  fi
else
  echo "ℹ️  No backend/.env yet — you'll need to create one:"
  echo "    cd backend && cp .env.example .env"
  echo "    Then add your Gemini API key"
fi

# ============================================================
# 8. Commit and push to GitHub
# ============================================================
echo ""
echo "📤 Committing changes and pushing to GitHub..."

# Make sure .env is gitignored (safety check)
if ! grep -q "^\.env$" .gitignore 2>/dev/null && ! grep -q "^\*\*/\.env$" .gitignore 2>/dev/null; then
  echo ".env" >> .gitignore
fi

git add .
git commit -m "Migrate from Anthropic to Google Gemini (free tier)" || echo "   (nothing to commit)"

# Only push if origin is configured
if git remote get-url origin > /dev/null 2>&1; then
  git push origin main
  echo "   ✅ Pushed to GitHub"
else
  echo "   ⚠️  No git remote configured — skipping push"
fi

# ============================================================
# Done
# ============================================================
echo ""
echo "✅ Migration complete!"
echo ""
echo "Next steps:"
echo "  1. cd backend"
echo "  2. source venv/bin/activate     # if you already have a venv"
echo "     OR"
echo "     python3 -m venv venv && source venv/bin/activate     # first time"
echo "  3. pip install -r requirements.txt"
echo "  4. uvicorn app.main:app --reload"
echo ""
echo "  In another terminal:"
echo "  5. cd frontend && npm install && npm run dev"
echo ""
echo "  Open http://localhost:3000 🎉"
