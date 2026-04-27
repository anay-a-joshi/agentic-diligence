"""Centralized prompts for all agents."""
from app.services.llm_client import MODEL_FLASH, MODEL_PRO

# Use Flash for per-agent fast calls; Pro for synthesis where quality matters most
AGENT_MODEL = MODEL_FLASH
SYNTHESIS_MODEL = MODEL_PRO
