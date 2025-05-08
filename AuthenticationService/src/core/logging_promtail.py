import logging
import sys

from src.core.config import settings

# Настройки логирования
logging.basicConfig(
    level=settings.log.level_value,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)
