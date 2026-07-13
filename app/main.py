import os
import logging
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask_cors import CORS
import jwt
from flask import Flask, g, jsonify, request
from prometheus_client import Counter, Gauge, generate_latest
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db_connection, init_db
from services.monitoring_service import check_website_health, get_server_metrics, check_ssl_expiry
from services.scheduler_service import start_scheduler
from services.incident_service import (
    create_incident,
    get_user_incidents,
    get_incident_by_id,
    resolve_incident,
    format_incident_row,
    get_incident_stats,
    has_open_incident_for_website,
    resolve_open_incidents_for_website,
)
from services.ai_service import analyze_incident_with_ai
from services.email_service import send_incident_email
from services.auto_heal_service import run_auto_heal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"], supports_credentials=True)

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
def handle_options():
    """Handle CORS preflight requests globally before any routing."""
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response


@app.before_request
def count_requests():
    REQUEST_COUNT.inc()


@app.route("/")
def home():
    return jsonify({
        "message": "AI Incident Response System is Running",
        "status": "ok"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/metrics")
def metrics():
    server_metrics = get_server_metrics()
    SERVER_CPU.set(server_metrics.get("cpu_percent", 0))
    SERVER_RAM.set(server_metrics.get("ram_percent", 0))
    SERVER_DISK.set(server_metrics.get("disk_percent", 0))

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


@app.after_request
def after_request(response):
    """Add CORS headers to all responses including 404s."""
    origin = request.headers.get("Origin", "")
    if origin in ["http://localhost:5173", "http://127.0.0.1:5173"]:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


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


# ===================== WEBSITE APIs =====================

@app.route("/websites", methods=["GET", "POST"])
@token_required()
def websites():
    user_id = g.current_user["user_id"]

    if request.method == "POST":
        data = request.get_json(silent=True) or {}

        name = data.get("name", "").strip()
        url = data.get("url", "").strip()

        if not name or not url:
            return jsonify({
                "error": "Website name and URL are required"
            }), 400

        if not url.startswith(("http://", "https://")):
            return jsonify({
                "error": "URL must start with http:// or https://"
            }), 400

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Check duplicate URL for same user
                cursor.execute(
                    "SELECT id FROM websites WHERE url = %s AND user_id = %s",
                    (url, user_id)
                )
                if cursor.fetchone():
                    return jsonify({
                        "error": "This URL is already being monitored"
                    }), 409

                cursor.execute(
                    """
                    INSERT INTO websites (user_id, name, url)
                    VALUES (%s, %s, %s)
                    RETURNING id, name, url, is_active, slow_threshold, request_timeout,
                              current_status, status_code, response_time_seconds,
                              last_error, last_checked_at, created_at
                    """,
                    (user_id, name, url)
                )

                row = cursor.fetchone()

            conn.commit()

        return jsonify({
            "message": "Website added successfully",
            "website": {
                "id": row[0],
                "name": row[1],
                "url": row[2],
                "is_active": row[3],
                "slow_threshold": row[4],
                "request_timeout": row[5],
                "current_status": row[6],
                "status_code": row[7],
                "response_time_seconds": row[8],
                "last_error": row[9],
                "last_checked_at": row[10].isoformat() if row[10] else None,
                "created_at": row[11].isoformat() if row[11] else None
            }
        }), 201

    # GET - list websites for current user
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, url, is_active, slow_threshold, request_timeout,
                       current_status, status_code, response_time_seconds,
                       last_error, last_checked_at, created_at
                FROM websites
                WHERE user_id = %s
                ORDER BY created_at DESC
                """,
                (user_id,)
            )

            rows = cursor.fetchall()

    return jsonify({
        "websites": [
            {
                "id": row[0],
                "name": row[1],
                "url": row[2],
                "is_active": row[3],
                "slow_threshold": row[4],
                "request_timeout": row[5],
                "current_status": row[6],
                "status_code": row[7],
                "response_time_seconds": row[8],
                "last_error": row[9],
                "last_checked_at": row[10].isoformat() if row[10] else None,
                "created_at": row[11].isoformat() if row[11] else None
            }
            for row in rows
        ]
    })


@app.route("/websites/<int:website_id>", methods=["GET", "PUT", "DELETE"])
@token_required()
def website_detail(website_id):
    user_id = g.current_user["user_id"]

    if request.method == "GET":
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, url, is_active, slow_threshold, request_timeout,
                           current_status, status_code, response_time_seconds,
                           last_error, last_checked_at, created_at
                    FROM websites
                    WHERE id = %s AND user_id = %s
                    """,
                    (website_id, user_id)
                )
                row = cursor.fetchone()

        if not row:
            return jsonify({"error": "Website not found"}), 404

        return jsonify({
            "website": {
                "id": row[0],
                "name": row[1],
                "url": row[2],
                "is_active": row[3],
                "slow_threshold": row[4],
                "request_timeout": row[5],
                "current_status": row[6],
                "status_code": row[7],
                "response_time_seconds": row[8],
                "last_error": row[9],
                "last_checked_at": row[10].isoformat() if row[10] else None,
                "created_at": row[11].isoformat() if row[11] else None
            }
        })

    elif request.method == "PUT":
        data = request.get_json(silent=True) or {}

        name = data.get("name", "").strip()
        url = data.get("url", "").strip()

        if not name or not url:
            return jsonify({"error": "Name and URL are required"}), 400

        if not url.startswith(("http://", "https://")):
            return jsonify({"error": "URL must start with http:// or https://"}), 400

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Verify ownership
                cursor.execute(
                    "SELECT id FROM websites WHERE id = %s AND user_id = %s",
                    (website_id, user_id)
                )
                if not cursor.fetchone():
                    return jsonify({"error": "Website not found"}), 404

                # Check duplicate URL for same user (excluding current)
                cursor.execute(
                    "SELECT id FROM websites WHERE url = %s AND user_id = %s AND id != %s",
                    (url, user_id, website_id)
                )
                if cursor.fetchone():
                    return jsonify({"error": "This URL is already being monitored"}), 409

                cursor.execute(
                    """
                    UPDATE websites
                    SET name = %s, url = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s AND user_id = %s
                    RETURNING id, name, url, is_active, slow_threshold, request_timeout,
                              current_status, status_code, response_time_seconds,
                              last_error, last_checked_at, created_at
                    """,
                    (name, url, website_id, user_id)
                )
                row = cursor.fetchone()
            conn.commit()

        return jsonify({
            "message": "Website updated successfully",
            "website": {
                "id": row[0],
                "name": row[1],
                "url": row[2],
                "is_active": row[3],
                "slow_threshold": row[4],
                "request_timeout": row[5],
                "current_status": row[6],
                "status_code": row[7],
                "response_time_seconds": row[8],
                "last_error": row[9],
                "last_checked_at": row[10].isoformat() if row[10] else None,
                "created_at": row[11].isoformat() if row[11] else None
            }
        })

    elif request.method == "DELETE":
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM websites WHERE id = %s AND user_id = %s RETURNING id",
                    (website_id, user_id)
                )
                deleted = cursor.fetchone()
            conn.commit()

        if not deleted:
            return jsonify({"error": "Website not found"}), 404

        return jsonify({"message": "Website deleted successfully"})


@app.route("/websites/<int:website_id>/toggle", methods=["PATCH"])
@token_required()
def toggle_website(website_id):
    user_id = g.current_user["user_id"]

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE websites
                SET is_active = NOT is_active, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s AND user_id = %s
                RETURNING id, is_active
                """,
                (website_id, user_id)
            )
            row = cursor.fetchone()
        conn.commit()

    if not row:
        return jsonify({"error": "Website not found"}), 404

    return jsonify({
        "message": "Website toggled",
        "id": row[0],
        "is_active": row[1]
    })


@app.route("/websites/<int:website_id>/check", methods=["POST"])
@token_required()
def check_website_now(website_id):
    user_id = g.current_user["user_id"]

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, url, slow_threshold, request_timeout, is_active
                FROM websites WHERE id = %s AND user_id = %s
                """,
                (website_id, user_id)
            )
            website = cursor.fetchone()

    if not website:
        return jsonify({"error": "Website not found"}), 404

    website_id, name, url, slow_threshold, request_timeout, is_active = website

    result = check_website_health(
        url=url,
        slow_threshold=slow_threshold or 2.0,
        timeout=request_timeout or 10
    )

    # Update website status in DB
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

    # Create incident if down/slow
    if result["status"] in ["slow", "down"] and is_active:
        if not has_open_incident_for_website(website_id, user_id):
            title = f"{name} Website {result['status'].upper()}"

            ai_summary = analyze_incident_with_ai(result)
            heal_report = "\n".join(run_auto_heal())

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
                "ai_summary": f"{ai_summary}\n\nAuto-Healing Actions:\n{heal_report}"
            })
    elif result["status"] == "up" and is_active:
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

    return jsonify({
        "message": "Check completed",
        "result": result
    })


# ===================== INCIDENT APIs =====================

@app.route("/incidents", methods=["GET"])
@token_required()
def incidents():
    user_id = g.current_user["user_id"]
    search = request.args.get("search")
    severity = request.args.get("severity")
    status = request.args.get("status")
    website_id = request.args.get("website_id", type=int)

    rows = get_user_incidents(
        user_id=user_id,
        search=search,
        severity=severity,
        status=status,
        website_id=website_id
    )

    stats = get_incident_stats(user_id)

    return jsonify({
        "total": len(rows),
        "incidents": [format_incident_row(r) for r in rows],
        "stats": {
            "total": stats[0],
            "open": stats[1],
            "critical": stats[2]
        }
    })


@app.route("/incidents/<int:incident_id>", methods=["GET"])
@token_required()
def incident_detail(incident_id):
    user_id = g.current_user["user_id"]
    row = get_incident_by_id(incident_id, user_id)

    if not row:
        return jsonify({"error": "Incident not found"}), 404

    return jsonify({"incident": format_incident_row(row)})


@app.route("/incidents/<int:incident_id>/resolve", methods=["PATCH"])
@token_required()
def resolve_incident_endpoint(incident_id):
    user_id = g.current_user["user_id"]
    success = resolve_incident(incident_id, user_id)

    if not success:
        return jsonify({"error": "Incident not found or already resolved"}), 404

    return jsonify({"message": "Incident resolved successfully"})


# ===================== MONITORING APIs =====================

@app.route("/server-metrics")
@token_required()
def server_metrics():
    return jsonify(get_server_metrics())


@app.route("/ssl-check")
@token_required()
def ssl_check():
    hostname = request.args.get("hostname", "")
    if not hostname:
        # Fallback: get hostname from user's first active website
        user_id = g.current_user["user_id"]
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT url FROM websites WHERE user_id = %s AND is_active = TRUE ORDER BY created_at DESC LIMIT 1",
                    (user_id,)
                )
                row = cursor.fetchone()
        if row:
            url = row[0]
            hostname = url.replace("https://", "").replace("http://", "").split("/")[0]
        else:
            return jsonify({"error": "No websites found. Please add a website first or provide a hostname parameter."}), 400
    return jsonify(check_ssl_expiry(hostname))


@app.route("/dashboard")
@token_required()
def dashboard():
    user_id = g.current_user["user_id"]

    # Get user's websites
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, url, is_active, current_status, status_code,
                       response_time_seconds, last_error, last_checked_at
                FROM websites
                WHERE user_id = %s
                ORDER BY created_at DESC
                """,
                (user_id,)
            )
            websites_rows = cursor.fetchall()

    # Get user's incident stats
    stats = get_incident_stats(user_id)

    # Get recent incidents
    recent_incidents = get_user_incidents(user_id, limit=5)

    # Get server metrics
    server_metrics_data = get_server_metrics()

    websites_list = [
        {
            "id": w[0],
            "name": w[1],
            "url": w[2],
            "is_active": w[3],
            "current_status": w[4],
            "status_code": w[5],
            "response_time_seconds": w[6],
            "last_error": w[7],
            "last_checked_at": w[8].isoformat() if w[8] else None
        }
        for w in websites_rows
    ]

    total_websites = len(websites_list)
    healthy = sum(1 for w in websites_list if w["current_status"] == "up")
    slow = sum(1 for w in websites_list if w["current_status"] == "slow")
    down = sum(1 for w in websites_list if w["current_status"] == "down")

    avg_response_time = None
    response_times = [w["response_time_seconds"] for w in websites_list if w["response_time_seconds"] is not None]
    if response_times:
        avg_response_time = round(sum(response_times) / len(response_times), 2)

    return jsonify({
        "websites": websites_list,
        "stats": {
            "total_websites": total_websites,
            "healthy": healthy,
            "slow": slow,
            "down": down,
            "total_incidents": stats[0],
            "open_incidents": stats[1],
            "critical_incidents": stats[2],
            "avg_response_time": avg_response_time
        },
        "recent_incidents": [format_incident_row(r) for r in recent_incidents],
        "metrics": server_metrics_data
    })


# ===================== ADMIN APIs =====================

@app.route("/admin/users", methods=["GET"])
@token_required("admin")
def admin_list_users():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, email, role, created_at
                FROM users
                ORDER BY created_at DESC
                """
            )
            rows = cursor.fetchall()

    return jsonify({
        "users": [
            {
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "role": row[3],
                "created_at": row[4].isoformat() if row[4] else None
            }
            for row in rows
        ]
    })


@app.route("/admin/users/<int:user_id>/role", methods=["PATCH"])
@token_required("admin")
def admin_change_role(user_id):
    data = request.get_json(silent=True) or {}
    new_role = data.get("role", "").strip()

    if new_role not in ("user", "admin"):
        return jsonify({"error": "Role must be 'user' or 'admin'"}), 400

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET role = %s WHERE id = %s RETURNING id",
                (new_role, user_id)
            )
            result = cursor.fetchone()
        conn.commit()

    if not result:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "Role updated successfully"})


# ===================== TEST EMAIL =====================

@app.route("/test-email", methods=["POST"])
@token_required()
def test_email():
    success = send_incident_email({
        "title": "Test Email from AI Incident Response Platform",
        "severity": "info",
        "status": "test",
        "ai_summary": "This is a test email to verify the email configuration."
    })

    if success:
        return jsonify({"message": "Test email sent successfully"})
    return jsonify({"error": "Failed to send test email"}), 500


if __name__ == "__main__":
    init_db()
    start_scheduler()

    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=debug_mode,
        use_reloader=False
    )