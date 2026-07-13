from apscheduler.schedulers.background import BackgroundScheduler
from services.website_workflow import run_website_workflow_for_website, get_active_websites
from services.server_workflow import run_server_workflow
from services.ssl_workflow import run_ssl_workflow

scheduler = BackgroundScheduler()


def scheduled_health_check():
    print("[Scheduler] Running health checks for all active websites...")

    websites = get_active_websites()

    if not websites:
        print("[Scheduler] No active websites to monitor")
        return

    for website in websites:
        try:
            result = run_website_workflow_for_website(website)

            if result:
                print(
                    f"[Scheduler] {website['name']} ({website['url']}) → "
                    f"{result['status']} ({result['severity']})"
                )
            else:
                print(
                    f"[Scheduler] {website['name']} skipped (inactive or error)"
                )

        except Exception as error:
            print(
                f"[Scheduler Error] {website['name']}: {error}"
            )

    # Run server and SSL workflows
    try:
        run_server_workflow()
    except Exception as error:
        print(f"[Scheduler Server Workflow Error] {error}")

    try:
        run_ssl_workflow()
    except Exception as error:
        print(f"[Scheduler SSL Workflow Error] {error}")


def start_scheduler():
    if scheduler.running:
        return

    scheduler.add_job(
        scheduled_health_check,
        trigger="interval",
        minutes=2,
        id="website_monitor",
        max_instances=1,
        replace_existing=True,
        coalesce=True
    )

    scheduler.start()
    print("[Scheduler] Started")