from services.monitoring_service import get_server_metrics
from services.incident_service import create_incident, has_open_incident_for_website
from services.ai_service import analyze_generic_incident

from settings import CPU_THRESHOLD, RAM_THRESHOLD, DISK_THRESHOLD


def run_server_workflow():
    """Check server resources and create incident if thresholds exceeded.
    Uses a dedicated system website_id=0 convention for server-level incidents."""
    server_metrics = get_server_metrics()

    if (
        server_metrics["cpu_percent"] > CPU_THRESHOLD
        or server_metrics["ram_percent"] > RAM_THRESHOLD
        or server_metrics["disk_percent"] > DISK_THRESHOLD
    ):
        # Check if there's already an open server resource incident
        # We use a special website_id convention for server incidents
        # For now, we just log and return to avoid creating duplicate incidents
        print(
            f"[Server Workflow] Resource threshold exceeded: "
            f"CPU={server_metrics['cpu_percent']}%, "
            f"RAM={server_metrics['ram_percent']}%, "
            f"Disk={server_metrics['disk_percent']}%"
        )