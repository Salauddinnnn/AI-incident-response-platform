import socket
import ssl
import time
from datetime import datetime

import psutil
import requests

# Reuse the same HTTP session for better performance
session = requests.Session()


def check_website_health(
    url,
    slow_threshold=2.0,
    timeout=10,
    retries=3
):
    """
    Check website availability with retry support.
    Prevents false alerts caused by temporary network issues.
    """

    last_error = None

    for attempt in range(retries):

        start_time = time.time()

        try:
            response = session.get(url, timeout=timeout)

            response_time = round(time.time() - start_time, 2)

            if response.status_code != 200:
                status = "down"
                severity = "critical"

            elif response_time > slow_threshold:
                status = "slow"
                severity = "warning"

            else:
                status = "up"
                severity = "normal"

            return {
                "url": url,
                "status_code": response.status_code,
                "response_time_seconds": response_time,
                "status": status,
                "severity": severity,
                "error": None
            }

        except Exception as error:

            last_error = str(error)

            # Retry after a short delay
            if attempt < retries - 1:
                time.sleep(2)

    return {
        "url": url,
        "status_code": None,
        "response_time_seconds": None,
        "status": "down",
        "severity": "critical",
        "error": last_error
    }


def get_server_metrics():
    """
    Return server resource usage.
    """

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent
    }


def check_ssl_expiry(hostname):
    """
    Check SSL certificate expiry.
    """

    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443), timeout=10) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
            cert = secure_sock.getpeercert()

    expiry_date = datetime.strptime(
        cert["notAfter"],
        "%b %d %H:%M:%S %Y %Z"
    )

    days_left = (expiry_date - datetime.utcnow()).days

    return {
        "hostname": hostname,
        "ssl_expiry_date": expiry_date.strftime("%Y-%m-%d"),
        "ssl_days_left": days_left
    }