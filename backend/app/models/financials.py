from pydantic import BaseModel


class FinancialSnapshot(BaseModel):
    revenue: float
    ebitda: float
    net_income: float
    free_cash_flow: float
    total_debt: float
    cash: float
    period: str
