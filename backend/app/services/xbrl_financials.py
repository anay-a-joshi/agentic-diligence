"""Fetches structured financial data from SEC's XBRL API.

This is the official SEC endpoint that exposes machine-readable financial
data extracted from every 10-K/10-Q. No scraping, no parsing — clean numbers.
"""
import httpx

from app.config import settings
from app.utils.logger import logger


XBRL_BASE = "https://data.sec.gov/api/xbrl/companyfacts"


def _cik_padded(cik: str) -> str:
    """SEC requires CIK as 10-digit zero-padded string."""
    return str(cik).zfill(10)


# Map our financial fields → XBRL US-GAAP concepts (in priority order)
# Companies use slightly different concepts; we try multiple
CONCEPT_MAP = {
    "revenue_usd_millions": [
        "Revenues",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "SalesRevenueNet",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
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
    """Find the most recent annual (FY) value for a concept.

    Returns (value_in_millions, fiscal_year) or (None, None) if not found.
    """
    us_gaap = facts.get("facts", {}).get("us-gaap", {})

    for concept in concept_aliases:
        entry = us_gaap.get(concept)
        if not entry:
            continue
        units = entry.get("units", {})
        # Prefer USD; fall back to shares for share counts
        for unit_key in ("USD", "USD/shares", "shares"):
            data_points = units.get(unit_key, [])
            if not data_points:
                continue
            # Filter to annual filings (form="10-K", fp="FY")
            annual = [
                dp for dp in data_points
                if dp.get("form") == "10-K" and dp.get("fp") == "FY"
            ]
            if not annual:
                continue
            # Pick the most recent by 'end' date
            latest = max(annual, key=lambda d: d.get("end", ""))
            val = latest.get("val")
            fy = latest.get("fy")
            if val is None:
                continue
            # Convert to millions for monetary values; leave shares alone if shares-unit
            if unit_key == "USD":
                return (val / 1_000_000.0, fy)
            elif unit_key == "shares":
                return (val / 1_000_000.0, fy)  # shares in millions too
            else:
                return (val, fy)
    return (None, None)


def fetch_structured_financials(cik: str) -> dict:
    """Fetch structured financials from SEC XBRL API.

    Returns a dict matching the FinancialData schema (numeric fields only).
    Does NOT include LLM-generated fields (drivers, risks, summary).
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
    fiscal_year_seen: int | None = None

    for field, aliases in CONCEPT_MAP.items():
        val, fy = _latest_annual_value(facts, aliases)
        if val is not None:
            # Round to integer for millions (cleaner for display/IC memo)
            out[field] = round(val)
            if fiscal_year_seen is None and fy is not None:
                fiscal_year_seen = fy

    if fiscal_year_seen:
        out["fiscal_year"] = fiscal_year_seen

    # Derive EBITDA if we have op income + D&A
    op_inc = out.pop("operating_income_usd_millions", None)
    da = out.pop("depreciation_amortization_usd_millions", None)
    if op_inc is not None and da is not None:
        out["ebitda_usd_millions"] = round(op_inc + da)
    elif op_inc is not None:
        # If no D&A available, EBITDA approximation is op income
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
                f"EBITDA=${out.get('ebitda_usd_millions')}M, FY={out.get('fiscal_year')}")

    return out
