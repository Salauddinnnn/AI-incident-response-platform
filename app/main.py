import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import Flask, g, jsonify, request
from prometheus_client import Counter, Gauge, generate_latest
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db_connection, init_db
from routes.monitoring import monitoring_bp
from services.monitoring_service import check_website_health, get_server_metrics
from services.scheduler_service import start_scheduler
from settings import MONITOR_URL, REQUEST_TIMEOUT, SLOW_THRESHOLD


app = Flask(__name__)
app.register_blueprint(monitoring_bp)


# Prometheus metrics
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
    "Server disk usage percent"
)


@app.before_request
def count_requests():
    REQUEST_COUNT.inc()


@app.route("/")
def home():
    return jsonify({
        "message": "AI Incident Response System is Running",
        "status": "ok"
    })


def update_prometheus_metrics():
    website_result = check_website_health(
        url=MONITOR_URL,
        slow_threshold=SLOW_THRESHOLD,
        timeout=REQUEST_TIMEOUT
    )

    server_metrics = get_server_metrics()

    WEBSITE_UP.set(
        1 if website_result.get("status") == "up" else 0
    )

    WEBSITE_RESPONSE_TIME.set(
        website_result.get("response_time_seconds") or 0
    )

    SERVER_CPU.set(server_metrics.get("cpu_percent", 0))
    SERVER_RAM.set(server_metrics.get("ram_percent", 0))
    SERVER_DISK.set(server_metrics.get("disk_percent", 0))


@app.route("/metrics")
def metrics():
    update_prometheus_metrics()

    return generate_latest(), 200, {
        "Content-Type": "text/plain; version=0.0.4"
    }


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({
            "error": "Name, email and password are required"
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters"
        }), 400

    password_hash = generate_password_hash(password)

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM users WHERE email = %s",
                (email,)
            )

            if cursor.fetchone():
                return jsonify({
                    "error": "Email already registered"
                }), 409

            cursor.execute(
                """
                INSERT INTO users (
                    name,
                    email,
                    password_hash,
                    role
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (name, email, password_hash, "user")
            )

            user_id = cursor.fetchone()[0]

        conn.commit()

    return jsonify({
        "message": "User registered successfully",
        "user_id": user_id
    }), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    email,
                    password_hash,
                    role
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            user = cursor.fetchone()

    if not user or not check_password_hash(user[3], password):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    jwt_secret = os.getenv("JWT_SECRET_KEY")

    if not jwt_secret:
        return jsonify({
            "error": "JWT secret is not configured"
        }), 500

    token = jwt.encode(
        {
            "user_id": user[0],
            "email": user[2],
            "role": user[4],
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)
        },
        jwt_secret,
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "role": user[4]
        }
    })


def token_required(required_role=None):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")

            if not auth_header.startswith("Bearer "):
                return jsonify({
                    "error": "Bearer token is missing"
                }), 401

            token = auth_header.split(" ", 1)[1].strip()

            try:
                payload = jwt.decode(
                    token,
                    os.getenv("JWT_SECRET_KEY"),
                    algorithms=["HS256"]
                )

            except jwt.ExpiredSignatureError:
                return jsonify({
                    "error": "Token expired"
                }), 401

            except jwt.InvalidTokenError:
                return jsonify({
                    "error": "Invalid token"
                }), 401

            if (
                required_role
                and payload.get("role") != required_role
            ):
                return jsonify({
                    "error": "Admin access required"
                }), 403

            g.current_user = payload

            return function(*args, **kwargs)

        return wrapper

    return decorator


@app.route("/profile")
@token_required()
def profile():
    return jsonify({
        "message": "Protected route accessed",
        "user": g.current_user
    })


@app.route("/admin-only")
@token_required("admin")
def admin_only():
    return jsonify({
        "message": "Admin access granted",
        "user": g.current_user
    })


if __name__ == "__main__":
    init_db()
    start_scheduler()

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True,
        use_reloader=False
    )