"""SEC XBRL structured financials fetcher — accuracy-first version.

Strategy:
- Fetch the companyfacts JSON (single API call, all concepts)
- For each target concept alias, gather ALL (fy, val, end, filed, form, fp) tuples
- Filter to annual full-year entries (form='10-K', fp='FY')
- Pick by HIGHEST fiscal year number (fy field), not by end-date string
- For ties, pick the entry with the LATEST 'filed' date (most-recently-amended)
- Verify the chosen fiscal year is consistent across all fields; warn if not
"""
from typing import Optional
import httpx

from app.config import settings
from app.utils.logger import logger


XBRL_BASE = "https://data.sec.gov/api/xbrl/companyfacts"


def _cik_padded(cik: str) -> str:
    return str(cik).zfill(10)


# Each entry: list of US-GAAP concept aliases that mean the same thing
CONCEPT_MAP = {
    "revenue_usd_millions": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
        "Revenues",
        "SalesRevenueNet",
    ],
    "net_income_usd_millions": [
        "NetIncomeLoss",
        "ProfitLoss",
    ],
    "operating_income_usd_millions": [
        "OperatingIncomeLoss",
    ],
    "depreciation_amortization_usd_millions": [
        "DepreciationDepletionAndAmortization",
        "DepreciationAndAmortization",
        "Depreciation",
    ],
    "cash_from_operations_usd_millions": [
        "NetCashProvidedByUsedInOperatingActivities",
    ],
    "capex_usd_millions": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
    ],
    "total_debt_usd_millions": [
        "LongTermDebtNoncurrent",
        "LongTermDebt",
        "DebtLongtermAndShorttermCombinedAmount",
    ],
    "cash_and_equivalents_usd_millions": [
        "CashAndCashEquivalentsAtCarryingValue",
        "Cash",
    ],
    "shares_outstanding_millions": [
        "CommonStockSharesOutstanding",
        "EntityCommonStockSharesOutstanding",
    ],
}


def _gather_annual_points(facts: dict, concept: str) -> list[dict]:
    """Gather all annual (10-K, FY) data points for a single concept.

    Returns list of dicts with: fy, val, end, filed, unit
    """
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    entry = us_gaap.get(concept)
    if not entry:
        return []

    out = []
    for unit_key, data_points in entry.get("units", {}).items():
        if unit_key not in ("USD", "shares"):
            continue
        for dp in data_points:
            if dp.get("form") != "10-K" or dp.get("fp") != "FY":
                continue
            if dp.get("val") is None or dp.get("fy") is None:
                continue
            out.append({
                "fy": int(dp["fy"]),
                "val": float(dp["val"]),
                "end": dp.get("end", ""),
                "filed": dp.get("filed", ""),
                "unit": unit_key,
            })
    return out


def _pick_latest(points: list[dict]) -> Optional[dict]:
    """Pick the point with the highest fy; tiebreak by latest filed date."""
    if not points:
        return None
    points_sorted = sorted(points, key=lambda p: (p["fy"], p["filed"]), reverse=True)
    return points_sorted[0]


def _pick_for_year(points: list[dict], target_fy: int) -> Optional[dict]:
    """Pick the data point for a specific fiscal year (used for YoY)."""
    matches = [p for p in points if p["fy"] == target_fy]
    if not matches:
        return None
    # Prefer most-recently-filed among matches (handles amendments)
    return sorted(matches, key=lambda p: p["filed"], reverse=True)[0]


def fetch_structured_financials(cik: str) -> dict:
    """Fetch & parse SEC XBRL company facts. Returns numeric financials."""
    cik_padded = _cik_padded(cik)
    url = f"{XBRL_BASE}/CIK{cik_padded}.json"
    headers = {"User-Agent": settings.sec_user_agent}

    logger.info(f"  Fetching XBRL companyfacts for CIK {cik_padded}...")
    try:
        with httpx.Client(timeout=20.0) as client:
            r = client.get(url, headers=headers)
            r.raise_for_status()
            facts = r.json()
    except Exception as e:
        logger.warning(f"  XBRL fetch failed: {e}")
        return {}

    # Step 1: For each field, find the BEST point across all alias concepts
    field_to_point: dict[str, dict] = {}
    for field, aliases in CONCEPT_MAP.items():
        # Gather candidates from all aliases
        candidates: list[dict] = []
        for concept in aliases:
            candidates.extend(_gather_annual_points(facts, concept))
        chosen = _pick_latest(candidates)
        if chosen is not None:
            field_to_point[field] = chosen

    # Step 2: Determine the dominant fiscal year (mode of fy across fields)
    if not field_to_point:
        logger.warning("  No XBRL data found")
        return {}

    fy_counts: dict[int, int] = {}
    for p in field_to_point.values():
        fy_counts[p["fy"]] = fy_counts.get(p["fy"], 0) + 1

    target_fy = max(fy_counts.keys())  # highest year that any field reached
    logger.info(f"  Target fiscal year: FY{target_fy} (year coverage: {dict(sorted(fy_counts.items(), reverse=True))})")

    # Step 3: For each field, prefer the data point AT target_fy (not just the freshest)
    # This ensures consistency across fields. Many old fields might not have FY{target_fy}
    # data yet because of late filings — fall back to their freshest.
    out: dict = {"fiscal_year": target_fy}
    fy_used: dict[str, int] = {}

    for field, aliases in CONCEPT_MAP.items():
        all_candidates: list[dict] = []
        for concept in aliases:
            all_candidates.extend(_gather_annual_points(facts, concept))

        # Try target year first, then fall back to latest available
        chosen = _pick_for_year(all_candidates, target_fy) or _pick_latest(all_candidates)
        if chosen is None:
            continue

        val = chosen["val"]
        # Convert to millions
        out[field] = round(val / 1_000_000.0)
        fy_used[field] = chosen["fy"]

    # Log per-field years so we can see consistency at a glance
    inconsistent = [f for f, fy in fy_used.items() if fy != target_fy]
    if inconsistent:
        logger.warning(f"  ⚠️  These fields use a different FY than {target_fy}: "
                       f"{ {f: fy_used[f] for f in inconsistent} }")
    else:
        logger.info(f"  ✅ All {len(fy_used)} fields aligned on FY{target_fy}")

    # Step 4: Compute YoY revenue growth using FY-1 revenue
    rev_now = out.get("revenue_usd_millions")
    if rev_now is not None:
        rev_aliases = CONCEPT_MAP["revenue_usd_millions"]
        rev_candidates: list[dict] = []
        for concept in rev_aliases:
            rev_candidates.extend(_gather_annual_points(facts, concept))
        prior = _pick_for_year(rev_candidates, target_fy - 1)
        if prior is not None and prior["val"] > 0:
            rev_prior_millions = prior["val"] / 1_000_000.0
            growth_pct = ((rev_now - rev_prior_millions) / rev_prior_millions) * 100.0
            out["revenue_growth_yoy_pct"] = round(growth_pct, 1)

    # Step 5: Derive EBITDA = Operating Income + D&A
    op_inc = out.pop("operating_income_usd_millions", None)
    da = out.pop("depreciation_amortization_usd_millions", None)
    if op_inc is not None and da is not None:
        out["ebitda_usd_millions"] = round(op_inc + da)
    elif op_inc is not None:
        out["ebitda_usd_millions"] = op_inc

    # Step 6: Derive FCF = CFO - CapEx
    cfo = out.pop("cash_from_operations_usd_millions", None)
    capex = out.pop("capex_usd_millions", None)
    if cfo is not None and capex is not None:
        # CapEx is reported as positive cash outflow; subtract it
        out["free_cash_flow_usd_millions"] = round(cfo - capex)
    elif cfo is not None:
        out["free_cash_flow_usd_millions"] = cfo

    # Step 7: Derive EBITDA margin
    rev = out.get("revenue_usd_millions")
    ebitda = out.get("ebitda_usd_millions")
    if rev and ebitda and rev > 0:
        out["ebitda_margin_pct"] = round(ebitda / rev * 100, 1)

    logger.info(
        f"  ✅ XBRL final: revenue=${out.get('revenue_usd_millions')}M, "
        f"NI=${out.get('net_income_usd_millions')}M, "
        f"EBITDA=${out.get('ebitda_usd_millions')}M, "
        f"FCF=${out.get('free_cash_flow_usd_millions')}M, "
        f"debt=${out.get('total_debt_usd_millions')}M, "
        f"cash=${out.get('cash_and_equivalents_usd_millions')}M, "
        f"shares={out.get('shares_outstanding_millions')}M, "
        f"YoY={out.get('revenue_growth_yoy_pct')}%, "
        f"FY={out.get('fiscal_year')}"
    )

    return out
