import asyncio
from collections.abc import AsyncGenerator

from aiosmtplib import SMTP

from src.core.config import SmtpConfig, settings
from src.core.logging_promtail import logger


class SmtpHelper:
    def __init__(self, config: SmtpConfig) -> None:
        self.semaphore = asyncio.Semaphore(config.pool_size)
        self.config = config
        self.client = SMTP(
            hostname=config.host,
            port=config.port,
            use_tls=config.use_tls,
            timeout=15.0,
        )

    async def get_smtp_client(self) -> AsyncGenerator[SMTP]:
        client = self.client
        async with self.semaphore:
            try:
                try:
                    await client.connect()
                except Exception as e:
                    logger.error(f"Cannot connect to SMTP server: {e}")
                try:
                    if self.config.host != 'maildev':
                        await client.login(
                            self.config.login,
                            self.config.password,
                        )
                except Exception as e:
                    logger.error(f"Cannot login to SMTP server: {e}")
                yield client
            finally:
                await client.quit()

smtp_helper = SmtpHelper(
    config=settings.smtp,
)
