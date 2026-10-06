from apscheduler.schedulers.blocking import BlockingScheduler
from main import main_pipeline
from config import HOURS_TIME, MINUTE_TIME, TIME_ZONE

scheduler =  BlockingScheduler()

scheduler.add_job(
    main_pipeline,
    trigger="cron",
    hour=HOURS_TIME,
    minute=MINUTE_TIME,
    timezone=TIME_ZONE,
    id="github_issues_etl",
    replace_existing=True,
    max_instances=1,
    coalesce=True,
)
print("scheduler is starting")
print(f"Scheduler Start At: {HOURS_TIME:02d}:{MINUTE_TIME:02d} ({TIME_ZONE})")

if __name__ == "__main__":
    scheduler.start()
