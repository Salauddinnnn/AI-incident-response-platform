from services.monitoring_service import check_ssl_expiry
from services.incident_service import create_incident
from services.ai_service import analyze_generic_incident

from settings import (
    MONITOR_NAME,
    MONITOR_URL,
    SSL_EXPIRY_THRESHOLD_DAYS,
    SSL_ALERT_STATE
)


def run_ssl_workflow():
    hostname = MONITOR_URL.replace("https://", "").replace("http://", "").replace("/", "")

    ssl_info = check_ssl_expiry(hostname)

    if ssl_info["ssl_days_left"] <= SSL_EXPIRY_THRESHOLD_DAYS:

        if not SSL_ALERT_STATE["is_ssl_incident_active"]:

            ai_summary = analyze_generic_incident(
                title=f"{MONITOR_NAME} SSL Certificate Expiry Warning",
                details=(
                    f"SSL certificate expires on {ssl_info['ssl_expiry_date']}. "
                    f"Days left: {ssl_info['ssl_days_left']}"
                )
            )

            create_incident(
                title=f"{MONITOR_NAME} SSL Certificate Expiry Warning",
                severity="warning",
                ai_summary=ai_summary
            )

            SSL_ALERT_STATE["is_ssl_incident_active"] = True

    else:
        SSL_ALERT_STATE["is_ssl_incident_active"] = False