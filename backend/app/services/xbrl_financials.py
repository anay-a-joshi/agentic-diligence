"""Fetches structured financial data from SEC's XBRL API.

Companies change their reporting concepts over time (e.g. Apple moved from
'Revenues' in 2018 to 'RevenueFromContractWithCustomerExcludingAssessedTax'
in 2019+). For each field, we scan ALL aliases and pick the entry with the
LATEST end date globally — never stale data.
"""
import httpx

from app.config import settings
from app.utils.logger import logger


XBRL_BASE = "https://data.sec.gov/api/xbrl/companyfacts"


def _cik_padded(cik: str) -> str:
    """SEC requires CIK as 10-digit zero-padded string."""
    return str(cik).zfill(10)


# Map our financial fields → ordered list of XBRL US-GAAP concepts (most-modern first)
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
        "LongTermDebt",
        "LongTermDebtNoncurrent",
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


def _latest_annual_value(facts: dict, concept_aliases: list[str]) -> tuple[float | None, int | None]:
    """Find the truly most-recent annual value across ALL concept aliases.

    Iterates every alias, every USD/shares unit, every annual data point,
    and picks the one with the latest `end` date globally.
    Returns (value_in_millions, fiscal_year) or (None, None).
    """
    us_gaap = facts.get("facts", {}).get("us-gaap", {})

    candidates: list[tuple[str, float, int | None, str]] = []  # (end_date, val, fy, unit)

    for concept in concept_aliases:
        entry = us_gaap.get(concept)
        if not entry:
            continue
        units = entry.get("units", {})
        for unit_key, data_points in units.items():
            if unit_key not in ("USD", "shares"):
                continue
            for dp in data_points:
                # We want full-year annual data: form 10-K and fp FY
                if dp.get("form") != "10-K" or dp.get("fp") != "FY":
                    continue
                val = dp.get("val")
                end = dp.get("end", "")
                fy = dp.get("fy")
                if val is None or not end:
                    continue
                candidates.append((end, val, fy, unit_key))

    if not candidates:
        return (None, None)

    # Pick the one with the latest end date
    candidates.sort(key=lambda x: x[0], reverse=True)
    latest_end, latest_val, latest_fy, latest_unit = candidates[0]

    # Convert to millions
    val_millions = latest_val / 1_000_000.0
    return (val_millions, latest_fy)


def fetch_structured_financials(cik: str) -> dict:
    """Fetch structured financials from SEC XBRL API.

    Returns a dict matching the FinancialData schema (numeric fields only).
    Always returns the freshest annual data available.
    """
    cik_padded = _cik_padded(cik)
    url = f"{XBRL_BASE}/CIK{cik_padded}.json"
    headers = {"User-Agent": settings.sec_user_agent}

    logger.info(f"  Fetching XBRL companyfacts for CIK {cik_padded}...")
    try:
        with httpx.Client(timeout=15.0) as client:
            r = client.get(url, headers=headers)
            r.raise_for_status()
            facts = r.json()
    except Exception as e:
        logger.warning(f"  XBRL fetch failed: {e}")
        return {}

    out: dict = {}
    fiscal_years_seen: list[int] = []

    for field, aliases in CONCEPT_MAP.items():
        val, fy = _latest_annual_value(facts, aliases)
        if val is not None:
            out[field] = round(val)
            if fy is not None:
                fiscal_years_seen.append(fy)

    # Use the most-recent fiscal year across all extracted fields
    if fiscal_years_seen:
        out["fiscal_year"] = max(fiscal_years_seen)

    # Derive EBITDA = Operating Income + D&A
    op_inc = out.pop("operating_income_usd_millions", None)
    da = out.pop("depreciation_amortization_usd_millions", None)
    if op_inc is not None and da is not None:
        out["ebitda_usd_millions"] = round(op_inc + da)
    elif op_inc is not None:
        out["ebitda_usd_millions"] = op_inc

    # Derive FCF = CFO - CapEx
    cfo = out.pop("cash_from_operations_usd_millions", None)
    capex = out.pop("capex_usd_millions", None)
    if cfo is not None and capex is not None:
        out["free_cash_flow_usd_millions"] = round(cfo - capex)
    elif cfo is not None:
        out["free_cash_flow_usd_millions"] = cfo

    # Derive EBITDA margin
    rev = out.get("revenue_usd_millions")
    ebitda = out.get("ebitda_usd_millions")
    if rev and ebitda and rev > 0:
        out["ebitda_margin_pct"] = round(ebitda / rev * 100, 1)

    logger.info(f"  XBRL extracted: revenue=${out.get('revenue_usd_millions')}M, "
                f"EBITDA=${out.get('ebitda_usd_millions')}M, "
                f"FCF=${out.get('free_cash_flow_usd_millions')}M, "
                f"FY={out.get('fiscal_year')}")

    return out
