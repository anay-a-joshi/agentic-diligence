from pydantic import BaseModel


class AnalysisResult(BaseModel):
    ticker: str
    company_name: str
    feasibility_score: int
    lbo_irr_base: float
    lbo_irr_bull: float
    lbo_irr_bear: float
    red_flags: list[str]
    ic_memo_url: str
    lbo_excel_url: str
