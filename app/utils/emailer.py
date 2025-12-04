import os
import aiosmtplib
from email.message import EmailMessage


SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASS = os.getenv('SMTP_PASS', '')


async def send_email(to_email: str, subject: str, body: str):
    if not SMTP_USER or not SMTP_PASS:
        print('SMTP not configured — skipping email')
        return False
    message = EmailMessage()
    message['From'] = SMTP_USER
    message['To'] = to_email
    message['Subject'] = subject
    message.set_content(body)


    await aiosmtplib.send(message, hostname=SMTP_HOST, port=SMTP_PORT, start_tls=True, username=SMTP_USER, password=SMTP_PASS)
    return True