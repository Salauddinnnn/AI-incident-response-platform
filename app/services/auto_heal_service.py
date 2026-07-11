import subprocess
import shutil


def run_auto_heal():
    actions = []

    # Docker check
    try:
        result = subprocess.run(
            ["docker", "ps"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            actions.append("Docker service healthy")
        else:
            actions.append("Docker service not responding")

    except Exception as e:
        actions.append(f"Docker check failed: {e}")

    # Disk usage check
    try:
        total, used, free = shutil.disk_usage("/")

        usage = (used / total) * 100

        if usage > 90:
            actions.append(f"Disk usage critical ({usage:.1f}%)")
        else:
            actions.append(f"Disk usage normal ({usage:.1f}%)")

    except Exception as e:
        actions.append(f"Disk check failed: {e}")

    # Flask health check
    try:
        result = subprocess.run(
            ["curl", "-s", "http://127.0.0.1:5001/"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if "AI Incident Response System" in result.stdout:
            actions.append("Flask application healthy")
        else:
            actions.append("Flask health check failed")

    except Exception as e:
        actions.append(f"Flask check failed: {e}")

    return actions