from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import analysis, chat, exports, health
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 DiligenceAI backend starting up...")
    yield
    logger.info("👋 DiligenceAI backend shutting down...")


app = FastAPI(
    title="DiligenceAI",
    description="Agentic AI for PE Take-Private Screening",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(analysis.router, prefix="/analyze", tags=["analysis"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(exports.router, prefix="/export", tags=["exports"])


@app.get("/")
async def root():
    return {"service": "DiligenceAI", "version": "0.1.0", "status": "ok"}
