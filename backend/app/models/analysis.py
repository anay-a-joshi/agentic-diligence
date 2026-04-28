"""Pydantic models for analysis output."""
from typing import Optional, Any
from pydantic import BaseModel, Field


class FinancialData(BaseModel):
    fiscal_year: Optional[int] = None
    revenue_usd_millions: Optional[float] = None
    ebitda_usd_millions: Optional[float] = None
    net_income_usd_millions: Optional[float] = None
    free_cash_flow_usd_millions: Optional[float] = None
    total_debt_usd_millions: Optional[float] = None
    cash_and_equivalents_usd_millions: Optional[float] = None
    shares_outstanding_millions: Optional[float] = None
    revenue_growth_yoy_pct: Optional[float] = None
    ebitda_margin_pct: Optional[float] = None
    key_drivers: list[str] = Field(default_factory=list)
    key_risks: list[str] = Field(default_factory=list)
    non_recurring_items: list[str] = Field(default_factory=list)
    summary: str = ""


class AnalysisResult(BaseModel):
    ticker: str
    company_name: str
    cik: str
    filings_summary: dict[str, int]
    financial: Optional[FinancialData] = None
    feasibility_score: Optional[int] = None
    feasibility_grade: Optional[str] = None
    feasibility_verdict: Optional[str] = None
    feasibility_breakdown: dict[str, Any] = Field(default_factory=dict)
    lbo_irr_base: Optional[float] = None
    lbo_irr_bull: Optional[float] = None
    lbo_irr_bear: Optional[float] = None
    lbo_moic_base: Optional[float] = None
    lbo_full: dict = Field(default_factory=dict)
    synthesis: dict = Field(default_factory=dict)
    red_flags: list[str] = Field(default_factory=list)
    ic_memo_url: str = ""
    lbo_excel_url: str = ""
    raw_findings: dict = Field(default_factory=dict)
