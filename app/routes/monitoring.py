from flask import Blueprint, jsonify

from services.incident_workflow import run_incident_workflow
from services.monitoring_service import get_server_metrics, check_ssl_expiry
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
    metrics = get_server_metrics()
    return jsonify(metrics)


@monitoring_bp.route("/ssl-check")
def ssl_check():
    hostname = get_hostname_from_url(MONITOR_URL)
    ssl_info = check_ssl_expiry(hostname)
    return jsonify(ssl_info)


@monitoring_bp.route("/status")
def status():
    return jsonify({
        "project": "AI Incident Response System",
        "monitor_name": MONITOR_NAME,
        "monitor_url": MONITOR_URL,
        "status": "running"
    })