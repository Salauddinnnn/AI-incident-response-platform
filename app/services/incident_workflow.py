from services.website_workflow import run_website_workflow
from services.server_workflow import run_server_workflow
from services.ssl_workflow import run_ssl_workflow


def run_incident_workflow():
    website_result = run_website_workflow()

    run_server_workflow()
    run_ssl_workflow()

    return website_result