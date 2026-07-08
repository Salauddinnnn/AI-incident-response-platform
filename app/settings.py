MONITOR_NAME = "SocialGrowthApp"
MONITOR_URL = "https://socialgrowthapp.in"

SLOW_THRESHOLD = 2.0
REQUEST_TIMEOUT = 10
ALERT_STATE = {
    "is_incident_active": False,
    "last_status": "up"
}
AUTO_HEAL_ENABLED = False
TARGET_CONTAINER_NAME = "your-container-name"
CPU_THRESHOLD = 80
RAM_THRESHOLD = 85
DISK_THRESHOLD = 90
RESOURCE_ALERT_STATE = {
    "is_resource_incident_active": False
}
SSL_EXPIRY_THRESHOLD_DAYS = 15

SSL_ALERT_STATE = {
    "is_ssl_incident_active": False
}