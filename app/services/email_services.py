
from email.mime.text import MIMEText
import smtplib
from app.core.config import settings


def send_otp_email(email: str, otp: str):
    subject = "your otp for shoplite account verification"
    body = f"""
        Hello,
        Your OTP for Shoplite account verification is: {otp}
        the otp is VALID FOR only 10 minutes
        regards
        Shoplite
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["To"] = email
    msg["From"] = settings.EMAIL_FROM
    try: 
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, email, msg.as_string())
    except Exception as e:
        print(e)