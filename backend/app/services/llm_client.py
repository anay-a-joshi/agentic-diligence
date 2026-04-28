"""Wraps Groq client (Llama 3.3 70B) with retry + JSON parsing helpers."""
import asyncio
import json
from groq import AsyncGroq
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.config import settings
from app.utils.logger import logger


# Groq model tiers — both free, both fast
MODEL_FLASH = "llama-3.3-70b-versatile"  # main workhorse: smart and free
MODEL_PRO = "llama-3.3-70b-versatile"    # same on free tier; could switch to a bigger paid model later

# Approx context window: 128K tokens. To stay safe, cap user content at ~80K chars
# (rough conversion: 4 chars per token => 80K chars ≈ 20K tokens).
MAX_INPUT_CHARS = 40_000


_client: AsyncGroq | None = None
_lock = asyncio.Lock()


def get_client() -> AsyncGroq:
    """Lazy singleton."""
    global _client
    if _client is None:
        if not settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY is not set. Add it to backend/.env")
        _client = AsyncGroq(api_key=settings.groq_api_key)
    return _client


# Free tier rate limit on Llama 3.3 70B is roughly 30 RPM.
# We serialize calls with a small delay to stay safely under this.
_MIN_INTERVAL_SECONDS = 2.5
_last_call_time: float = 0.0


async def _throttle():
    """Ensure we don't hammer Groq's free-tier rate limit."""
    global _last_call_time
    async with _lock:
        now = asyncio.get_event_loop().time()
        elapsed = now - _last_call_time
        if elapsed < _MIN_INTERVAL_SECONDS:
            await asyncio.sleep(_MIN_INTERVAL_SECONDS - elapsed)
        _last_call_time = asyncio.get_event_loop().time()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=4, max=20),
    reraise=True,
)
async def call_llm(
    prompt: str,
    system: str = "",
    model: str = MODEL_FLASH,
    max_tokens: int = 4096,
    temperature: float = 0.2,
) -> str:
    """Send a prompt to Groq's Llama and return the text response."""
    await _throttle()

    # Truncate user content to stay within context window
    if len(prompt) > MAX_INPUT_CHARS:
        logger.warning(f"Truncating prompt from {len(prompt)} to {MAX_INPUT_CHARS} chars")
        prompt = prompt[:MAX_INPUT_CHARS]

    client = get_client()

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        raise


async def call_llm_json(prompt: str, system: str = "", model: str = MODEL_FLASH) -> dict:
    """Ask the model for JSON and parse it. Uses Groq's native JSON mode."""
    await _throttle()

    if len(prompt) > MAX_INPUT_CHARS:
        logger.warning(f"Truncating prompt from {len(prompt)} to {MAX_INPUT_CHARS} chars")
        prompt = prompt[:MAX_INPUT_CHARS]

    client = get_client()

    messages = []
    # Groq's JSON mode requires the word "json" in the system or user prompt
    if system:
        messages.append({"role": "system", "content": system + "\n\nAlways respond in JSON format."})
    else:
        messages.append({"role": "system", "content": "Always respond in JSON format."})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=4096,
        temperature=0.0,
        response_format={"type": "json_object"},
    )
    raw = response.choices[0].message.content or "{}"
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: try to strip code fences if present
        cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(cleaned)
