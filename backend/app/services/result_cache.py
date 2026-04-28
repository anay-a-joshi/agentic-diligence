"""File-based cache for analysis outputs.

Survives LLM rate limits. Quality-gated: only caches results where
5+/8 agents returned real data. TTL: 24 hours.
"""
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Any

log = logging.getLogger("diligence-ai")
CACHE_DIR = Path(__file__).parent.parent.parent / "cache"
CACHE_DIR.mkdir(exist_ok=True, parents=True)


def _path(ticker: str) -> Path:
    return CACHE_DIR / f"{ticker.upper()}_latest.json"


def load_cached(ticker: str, max_age_hours: int = 24) -> Optional[dict]:
    """Return cached result dict if exists and fresh, else None."""
    p = _path(ticker)
    if not p.exists():
        return None
    try:
        age = datetime.now() - datetime.fromtimestamp(p.stat().st_mtime)
        if age > timedelta(hours=max_age_hours):
            log.info(f"  Cache expired for {ticker} (age: {age})")
            return None
        return json.loads(p.read_text())
    except Exception as e:
        log.info(f"  Cache read failed for {ticker}: {e}")
        return None


def save_cached(ticker: str, result: Any) -> None:
    """Persist result. Only saves high-quality runs (5+/8 agents OK)."""
    try:
        if hasattr(result, "model_dump"):
            data = result.model_dump()
        elif hasattr(result, "dict"):
            data = result.dict()
        elif isinstance(result, dict):
            data = result
        else:
            return

        # Quality gate: count agents that returned substantive data
        raw = data.get("raw_findings", {}) or {}
        agents_ok = 0
        for k, v in raw.items():
            if isinstance(v, dict):
                payload = v.get("data") or {}
                if payload and len(str(payload)) > 100:
                    agents_ok += 1

        if agents_ok < 5:
            log.info(f"  ⚠️  NOT caching {ticker}: only {agents_ok}/8 agents had data (need 5+)")
            return

        _path(ticker).write_text(json.dumps(data, default=str, indent=2))
        log.info(f"  ✅ Cached {ticker} ({agents_ok}/8 agents OK, valid 24h)")
    except Exception as e:
        log.info(f"  Cache write failed: {e}")


def clear_cache(ticker: Optional[str] = None) -> int:
    """Clear cache for ticker, or all if ticker is None."""
    if ticker:
        p = _path(ticker)
        if p.exists():
            p.unlink()
            return 1
        return 0
    count = 0
    for f in CACHE_DIR.glob("*_latest.json"):
        f.unlink()
        count += 1
    return count
