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
            title = f"{MONITOR_NAME} Website {result['status'].upper()}"

            ai_summary = analyze_incident_with_ai(result)
            heal_summary = "\n".join(run_auto_heal())

            complete_summary = (
                f"{ai_summary}\n\n"
                f"Auto-Healing Actions:\n{heal_summary}"
            )

            create_incident(
                title=title,
                severity=result["severity"],
                ai_summary=complete_summary
            )

            send_incident_email({
                "title": title,
                "severity": result["severity"],
                "status": result["status"],
                "ai_summary": complete_summary
            })

            ALERT_STATE["is_incident_active"] = True

    else:
        if ALERT_STATE["is_incident_active"]:
            resolve_open_incidents()

            send_incident_email({
                "title": f"{MONITOR_NAME} Website Recovered",
                "severity": "normal",
                "status": "resolved",
                "ai_summary": (
                    f"{MONITOR_NAME} is healthy again.\n\n"
                    f"Website: {result['url']}\n"
                    f"Response Time: "
                    f"{result['response_time_seconds']} sec"
                )
            })

        ALERT_STATE["is_incident_active"] = False

    return result