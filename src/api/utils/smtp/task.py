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


# from .smtp_email_backend import SmtpEmailBackend
#
# def send_email_newsletter():
#     email_backend = SmtpEmailBackend(
#         smtp_server="localhost",
#         smtp_port=1025,
#         from_email="noreply@shop.com",
#     )
#
#     email_backend.send_email(
#         recipient="example@gmail.com", subject="123", body="Hello!"
#     )
