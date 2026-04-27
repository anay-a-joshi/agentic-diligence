"""Wraps Anthropic / OpenAI clients with retry + telemetry."""
import anthropic
from app.config import settings


client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)


async def call_llm(prompt: str, system: str = "", model: str = "claude-opus-4-5") -> str:
    response = await client.messages.create(
        model=model,
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
