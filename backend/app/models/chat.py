from pydantic import BaseModel


class ChatRequest(BaseModel):
    ticker: str
    message: str


class ChatResponse(BaseModel):
    response: str
    citations: list[str] = []
