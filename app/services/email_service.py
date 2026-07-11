import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import EMAIL_USER, EMAIL_PASSWORD, ALERT_EMAIL

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_incident_email(incident):
    """
    Send AI Incident Alert Email
    """

    subject = f"🚨 {incident['severity'].upper()} Incident - {incident['title']}"

    body = f"""
AI INCIDENT RESPONSE PLATFORM

Incident:
{incident['title']}

Severity:
{incident['severity']}

Status:
{incident['status']}

AI Analysis:

{incident['ai_summary']}

Generated Automatically by AI Incident Response Platform
"""

    message = MIMEMultipart()
    message["From"] = EMAIL_USER
    message["To"] = ALERT_EMAIL
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)

            server.sendmail(
                EMAIL_USER,
                ALERT_EMAIL,
                message.as_string()
            )

        print("Email Alert Sent")
        return True

    except Exception as e:
        print(e)
        return False