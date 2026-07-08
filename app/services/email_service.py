import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import EMAIL_USER, EMAIL_PASSWORD, ALERT_EMAIL

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_incident_email(subject, body):
    """
    Send an incident notification email.
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

        print("✅ Email Alert Sent Successfully")

        return True

    except Exception as error:
        print(f"❌ Email Error: {error}")
        return False