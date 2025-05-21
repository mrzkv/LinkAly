import logging

from src.core.config import settings

# Logging Settings
logging.basicConfig(
    level=settings.log.level_value,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger()
