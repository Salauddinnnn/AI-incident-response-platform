from flask import Flask
from prometheus_client import Counter, Gauge, generate_latest

from routes.monitoring import monitoring_bp
from database.db import init_db
from services.scheduler_service import start_scheduler
from services.monitoring_service import check_website_health, get_server_metrics
from settings import MONITOR_URL, SLOW_THRESHOLD, REQUEST_TIMEOUT


app = Flask(__name__)
app.register_blueprint(monitoring_bp)


REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of requests received"
)

WEBSITE_UP = Gauge(
    "website_up",
    "Website availability: 1 means up, 0 means down"
)

WEBSITE_RESPONSE_TIME = Gauge(
    "website_response_time_seconds",
    "Website response time in seconds"
)

SERVER_CPU = Gauge(
    "server_cpu_percent",
    "Server CPU usage percent"
)

SERVER_RAM = Gauge(
    "server_ram_percent",
    "Server RAM usage percent"
)

SERVER_DISK = Gauge(
    "server_disk_percent",
    "Server Disk usage percent"
)


@app.before_request
def count_requests():
    REQUEST_COUNT.inc()


@app.route("/")
def home():
    return {
        "message": "AI Incident Response System is Running",
        "status": "ok"
    }


def update_prometheus_metrics():
    # Only collect metrics here. Do not trigger AI, email, or incident workflow.
    website_result = check_website_health(
        url=MONITOR_URL,
        slow_threshold=SLOW_THRESHOLD,
        timeout=REQUEST_TIMEOUT
    )

    server_metrics = get_server_metrics()

    WEBSITE_UP.set(1 if website_result["status"] == "up" else 0)
    WEBSITE_RESPONSE_TIME.set(website_result["response_time_seconds"] or 0)

    SERVER_CPU.set(server_metrics["cpu_percent"])
    SERVER_RAM.set(server_metrics["ram_percent"])
    SERVER_DISK.set(server_metrics["disk_percent"])


@app.route("/metrics")
def metrics():
    update_prometheus_metrics()
    return generate_latest(), 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
    init_db()
    start_scheduler()
    app.run(host="0.0.0.0", port=5001, debug=True)