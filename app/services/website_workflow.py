from services.monitoring_service import check_website_health
from services.incident_service import create_incident, resolve_open_incidents
from services.ai_service import analyze_incident_with_ai
from services.email_service import send_incident_email
from services.auto_heal_service import run_auto_heal

from settings import (
    MONITOR_NAME,
    MONITOR_URL,
    SLOW_THRESHOLD,
    REQUEST_TIMEOUT,
    ALERT_STATE
)


def run_website_workflow():
    result = check_website_health(
        url=MONITOR_URL,
        slow_threshold=SLOW_THRESHOLD,
        timeout=REQUEST_TIMEOUT
    )

    if result["status"] in ["slow", "down"]:
        if not ALERT_STATE["is_incident_active"]:
            ai_summary = analyze_incident_with_ai(result)
            heal_summary = "\n".join(run_auto_heal())

            create_incident(
                title=f"{MONITOR_NAME} Website {result['status'].upper()}",
                severity=result["severity"],
                ai_summary=f"{ai_summary}\n\nAuto-Healing Actions:\n{heal_summary}"
            )

            send_incident_email(
                subject=f"[{result['severity'].upper()}] {MONITOR_NAME} Incident",
                body=f"""Website: {result['url']}

Status: {result['status']}
Severity: {result['severity']}
Status Code: {result['status_code']}
Response Time: {result['response_time_seconds']} sec

AI Analysis:

{ai_summary}

Auto-Healing Report:

{heal_summary}
"""
            )

            ALERT_STATE["is_incident_active"] = True

    else:
        if ALERT_STATE["is_incident_active"]:
            send_incident_email(
                subject=f"[RECOVERED] {MONITOR_NAME}",
                body=f"""{MONITOR_NAME} is healthy again.

Website: {result['url']}
Status: {result['status']}
Response Time: {result['response_time_seconds']} sec
"""
            )

            resolve_open_incidents()

        ALERT_STATE["is_incident_active"] = False

    return result