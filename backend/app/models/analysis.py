"""Pydantic models for analysis API responses."""
from typing import Any
from pydantic import BaseModel, Field


class FinancialData(BaseModel):
    """Output of the Financial Agent."""
    fiscal_year: int | None = None
    revenue_usd_millions: float | None = None
    ebitda_usd_millions: float | None = None
    net_income_usd_millions: float | None = None
    free_cash_flow_usd_millions: float | None = None
    total_debt_usd_millions: float | None = None
    cash_and_equivalents_usd_millions: float | None = None
    shares_outstanding_millions: float | None = None
    revenue_growth_yoy_pct: float | None = None
    ebitda_margin_pct: float | None = None
    key_drivers: list[str] = Field(default_factory=list)
    key_risks: list[str] = Field(default_factory=list)
    non_recurring_items: list[str] = Field(default_factory=list)
    summary: str | None = None


class FilingMetadata(BaseModel):
    form: str
    filing_date: str
    accession_number: str
    url: str


class AnalysisResult(BaseModel):
    """Top-level response shape returned to the frontend."""
    ticker: str
    company_name: str
    cik: str = ""
    filings_summary: dict[str, int] = Field(default_factory=dict)  # form -> count
    financial: FinancialData | None = None
    # Future fields for later phases:
    feasibility_score: int | None = None
    lbo_irr_base: float | None = None
    lbo_irr_bull: float | None = None
    lbo_irr_bear: float | None = None
    red_flags: list[str] = Field(default_factory=list)
    ic_memo_url: str = ""
    lbo_excel_url: str = ""
    raw_findings: dict[str, Any] = Field(default_factory=dict)
