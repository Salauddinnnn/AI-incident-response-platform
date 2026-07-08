from apscheduler.schedulers.background import BackgroundScheduler
from services.incident_workflow import run_incident_workflow

scheduler = BackgroundScheduler()


def scheduled_health_check():
    try:
        result = run_incident_workflow()
        print(
            f"[Scheduler] {result['url']} → "
            f"{result['status']} ({result['severity']})"
        )

    except Exception as error:
        print(f"[Scheduler Error] {error}")


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