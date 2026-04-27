"""Shared FastAPI dependencies (auth, rate limiting, etc.)"""
from fastapi import Header, HTTPException


async def verify_user_agent(user_agent: str = Header(default="")):
    if not user_agent:
        raise HTTPException(status_code=400, detail="User-Agent required")
    return user_agent
