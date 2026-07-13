from services.website_workflow import run_website_workflow_for_website, get_active_websites
from services.server_workflow import run_server_workflow
from services.ssl_workflow import run_ssl_workflow


def run_incident_workflow():
    """Run the monitoring workflow for all active websites.
    Returns the result of the first website check for backward compatibility."""
    websites = get_active_websites()

    first_result = None
    for website in websites:
        result = run_website_workflow_for_website(website)
        if first_result is None and result is not None:
            first_result = result

    run_server_workflow()
    run_ssl_workflow()

    return first_result or {"status": "unknown", "severity": "info", "url": ""}