from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    ticker: str
    message: str


class ChatResponse(BaseModel):
    response: str
    citations: list[str] = []


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # TODO: wire to RAG agent over cached filings
    return ChatResponse(
        response=f"[Stub] You asked about {request.ticker}: {request.message}",
        citations=[],
    )
