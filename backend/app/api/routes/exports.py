from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/pdf/{ticker}")
async def export_pdf(ticker: str):
    # TODO: generate via app.generators.ic_memo_pdf
    return {"message": f"PDF export for {ticker} — not yet implemented"}


@router.get("/xlsx/{ticker}")
async def export_xlsx(ticker: str):
    # TODO: generate via app.generators.lbo_excel
    return {"message": f"Excel export for {ticker} — not yet implemented"}
