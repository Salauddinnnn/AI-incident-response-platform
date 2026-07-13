from services.monitoring_service import check_ssl_expiry
from settings import SSL_EXPIRY_THRESHOLD_DAYS


def run_ssl_workflow():
    """SSL expiry check is now done per-website via the check endpoint.
    This function is kept for backward compatibility."""
    pass