from email.mime.text import MIMEText

import aiosmtplib


class SMTPRepository:
    def __init__(self, conn: aiosmtplib.SMTP) -> None:
        self.conn = conn

    async def send(self, message: MIMEText) -> None:
        await self.conn.send_message(message)
