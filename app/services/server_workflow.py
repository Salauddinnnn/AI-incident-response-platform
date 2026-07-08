from services.monitoring_service import get_server_metrics
from services.incident_service import create_incident
from services.ai_service import analyze_generic_incident

from settings import (
    MONITOR_NAME,
    CPU_THRESHOLD,
    RAM_THRESHOLD,
    DISK_THRESHOLD,
    RESOURCE_ALERT_STATE
)


def run_server_workflow():
    server_metrics = get_server_metrics()

    if (
        server_metrics["cpu_percent"] > CPU_THRESHOLD
        or server_metrics["ram_percent"] > RAM_THRESHOLD
        or server_metrics["disk_percent"] > DISK_THRESHOLD
    ):

        if not RESOURCE_ALERT_STATE["is_resource_incident_active"]:

            ai_summary = analyze_generic_incident(
                title=f"{MONITOR_NAME} Server Resource Alert",
                details=(
                    f"CPU: {server_metrics['cpu_percent']}%, "
                    f"RAM: {server_metrics['ram_percent']}%, "
                    f"Disk: {server_metrics['disk_percent']}%"
                )
            )

            create_incident(
                title=f"{MONITOR_NAME} Server Resource Alert",
                severity="critical",
                ai_summary=ai_summary
            )

            RESOURCE_ALERT_STATE["is_resource_incident_active"] = True

    else:
        RESOURCE_ALERT_STATE["is_resource_incident_active"] = False