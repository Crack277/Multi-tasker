from email.message import EmailMessage

import aiosmtplib
from pydantic import EmailStr


async def send_email(
    recipient: EmailStr,
    body: str,
    subject: str = "CONFIRM CODE",
):
    admin_email = "admin@site.com"

    message = EmailMessage()
    message["From"] = "admin@site.com"
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        sender=admin_email,
        recipients=[recipient],
        hostname="localhost",
        port=1025,
    )

