from flask import Blueprint, jsonify

from database.db import get_db_connection
from services.incident_workflow import run_incident_workflow
from services.monitoring_service import check_ssl_expiry, get_server_metrics
from settings import MONITOR_NAME, MONITOR_URL


monitoring_bp = Blueprint("monitoring", __name__)


def get_hostname_from_url(url):
    return url.replace("https://", "").replace("http://", "").split("/")[0]


@monitoring_bp.route("/health-check")
@monitoring_bp.route("/check-socialgrowth")
def check_website():
    result = run_incident_workflow()
    return jsonify(result)


@monitoring_bp.route("/server-metrics")
def server_metrics():
    return jsonify(get_server_metrics())


@monitoring_bp.route("/ssl-check")
def ssl_check():
    hostname = get_hostname_from_url(MONITOR_URL)
    return jsonify(check_ssl_expiry(hostname))


@monitoring_bp.route("/incidents")
def incident_history():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    title,
                    severity,
                    status,
                    ai_summary,
                    created_at
                FROM incidents
                ORDER BY created_at DESC
                LIMIT 100
            """)

            rows = cursor.fetchall()

    incidents = [
        {
            "id": row[0],
            "title": row[1],
            "severity": row[2],
            "status": row[3],
            "ai_summary": row[4],
            "created_at": row[5].isoformat() if row[5] else None
        }
        for row in rows
    ]

    return jsonify({
        "total": len(incidents),
        "incidents": incidents
    })


@monitoring_bp.route("/status")
def status():
    return jsonify({
        "project": "AI Incident Response System",
        "monitor_name": MONITOR_NAME,
        "monitor_url": MONITOR_URL,
        "status": "running"
    })