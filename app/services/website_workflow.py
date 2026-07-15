import logging

from database.db import get_db_connection
from services.monitoring_service import check_website_health
from services.incident_service import (
    create_incident,
    has_open_incident_for_website,
    resolve_open_incidents_for_website,
)
from services.ai_service import analyze_incident_with_ai
from services.email_service import send_incident_email
from services.auto_heal_service import run_auto_heal

logger = logging.getLogger(__name__)


def run_website_workflow_for_website(website):
    """
    Run monitoring workflow for a single website.
    website must be a dict with keys: id, user_id, name, url, slow_threshold, request_timeout, is_active
    """
    website_id = website["id"]
    user_id = website["user_id"]
    name = website["name"]
    url = website["url"]
    slow_threshold = website.get("slow_threshold") or 2.0
    request_timeout = website.get("request_timeout") or 10
    is_active = website.get("is_active", True)

    if not is_active:
        return None

    if not user_id:
        logger.warning(f"Skipping website {name} ({url}) - no user_id assigned")
        return None

    try:
        result = check_website_health(
            url=url,
            slow_threshold=slow_threshold,
            timeout=request_timeout
        )
    except Exception as e:
        logger.error(f"Health check failed for {name} ({url}): {e}")
        return None

    # Update website status in DB
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE websites
                    SET current_status = %s,
                        status_code = %s,
                        response_time_seconds = %s,
                        last_error = %s,
                        last_checked_at = CURRENT_TIMESTAMP,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (
                        result["status"],
                        result["status_code"],
                        result["response_time_seconds"],
                        result["error"],
                        website_id
                    )
                )
            conn.commit()
    except Exception as e:
        logger.error(f"Failed to update website status for {name}: {e}")

    # Handle incident creation/resolution
    try:
        if result["status"] in ["slow", "down"]:
            if not has_open_incident_for_website(website_id, user_id):
                title = f"{name} Website {result['status'].upper()}"

                ai_summary = analyze_incident_with_ai(result)
                heal_report = "\n".join(run_auto_heal())

                complete_summary = (
                    f"{ai_summary}\n\n"
                    f"Auto-Healing Actions:\n{heal_report}"
                )

                create_incident(
                    user_id=user_id,
                    website_id=website_id,
                    title=title,
                    severity=result["severity"],
                    ai_summary=ai_summary,
                    auto_heal_report=heal_report
                )

                send_incident_email({
                    "title": title,
                    "severity": result["severity"],
                    "status": result["status"],
                    "ai_summary": complete_summary
                })
        else:
            resolved = resolve_open_incidents_for_website(website_id, user_id)
            if resolved > 0:
                send_incident_email({
                    "title": f"{name} Website Recovered",
                    "severity": "normal",
                    "status": "resolved",
                    "ai_summary": (
                        f"{name} is healthy again.\n\n"
                        f"Website: {url}\n"
                        f"Response Time: {result['response_time_seconds']} sec"
                    )
                })
    except Exception as e:
        logger.error(f"Incident workflow failed for {name}: {e}")

    return result


def get_active_websites():
    """Get all active websites from database."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, user_id, name, url, slow_threshold, request_timeout, is_active
                    FROM websites
                    WHERE is_active = TRUE
                    """
                )
                rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "user_id": row[1],
                "name": row[2],
                "url": row[3],
                "slow_threshold": row[4] if row[4] is not None else 2.0,
                "request_timeout": row[5] if row[5] is not None else 10,
                "is_active": row[6]
            }
            for row in rows
        ]
    except Exception as e:
        logger.error(f"Failed to get active websites: {e}")
        return []