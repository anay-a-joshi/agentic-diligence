import logging
import sys

from app.config import settings


logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("diligence-ai")
