"""Wraps Google Gemini client with retry + telemetry."""
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings
from app.utils.logger import logger


# Gemini model tiers — Flash is fast/free, Pro is higher quality
MODEL_FLASH = "gemini-2.0-flash-exp"   # use for cheap, fast agent calls
MODEL_PRO = "gemini-1.5-pro"           # use for synthesis & long-context work


_client: genai.Client | None = None


def get_client() -> genai.Client:
    """Lazy singleton — created on first use so missing keys don't crash startup."""
    global _client
    if _client is None:
        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to backend/.env"
            )
        _client = genai.Client(api_key=settings.gemini_api_key)
    return _client


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True,
)
async def call_llm(
    prompt: str,
    system: str = "",
    model: str = MODEL_FLASH,
    max_tokens: int = 4096,
    temperature: float = 0.2,
) -> str:
    """
    Send a prompt to Gemini and return the text response.

    Args:
        prompt: User-facing prompt content
        system: System instruction (optional)
        model: Gemini model identifier — defaults to fast/free Flash
        max_tokens: Output cap
        temperature: 0.0 = deterministic, 1.0 = creative
    """
    client = get_client()

    config = types.GenerateContentConfig(
        max_output_tokens=max_tokens,
        temperature=temperature,
    )
    if system:
        config.system_instruction = system

    try:
        response = await client.aio.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
        return response.text or ""
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise


async def call_llm_json(prompt: str, system: str = "", model: str = MODEL_FLASH) -> dict:
    """Convenience wrapper that asks Gemini to return JSON and parses it."""
    import json

    full_prompt = (
        f"{prompt}\n\n"
        "Respond with ONLY a valid JSON object. "
        "No markdown fences, no preamble, no explanation."
    )
    raw = await call_llm(full_prompt, system=system, model=model, temperature=0.0)
    # Strip code fences if the model included them anyway
    cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(cleaned)
