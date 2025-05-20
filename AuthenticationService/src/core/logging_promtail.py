import logging

from src.core.config import settings

# Настройки логирования
logging.basicConfig(
    level=settings.log.level_value,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
