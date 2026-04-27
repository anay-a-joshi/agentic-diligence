"""POST /analyze/{ticker} — kick off the multi-agent pipeline."""
from fastapi import APIRouter, HTTPException

from app.agents.orchestrator import run_full_analysis
from app.models.analysis import AnalysisResult
from app.utils.logger import logger

router = APIRouter()


@router.post("/{ticker}", response_model=AnalysisResult)
async def analyze_ticker(ticker: str):
    """Trigger the full multi-agent pipeline for a given ticker."""
    ticker = ticker.upper().strip()
    if not ticker.isalpha() or len(ticker) > 5:
        raise HTTPException(status_code=400, detail="Invalid ticker format")
    try:
        result = await run_full_analysis(ticker)
        return result
    except Exception as e:
        logger.exception(f"Analysis failed for {ticker}")
        raise HTTPException(status_code=500, detail=str(e))
