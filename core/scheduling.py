import atexit
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings

logger = logging.getLogger(__name__)

_scheduler = None 

def start_scheduler():
    global _scheduler
    if not getattr(settings, "SCHEDULER_ENABLED", False):
        logger.info("Scheduler disabled by settings.")
        return
    if _scheduler:
        return

    from insurance.jobs import log_expired_policies_once 

    interval = int(getattr(settings, "SCHEDULER_INTERVAL_MINUTES", 10))
    _scheduler = BackgroundScheduler(
        timezone=settings.TIME_ZONE,
        job_defaults={"coalesce": True, "max_instances": 1, "misfire_grace_time": 300},
    )
    _scheduler.add_job(
        log_expired_policies_once,
        IntervalTrigger(minutes=interval),
        id="policy-expiry-logger",
        replace_existing=True,
        coalesce=True,
        misfire_grace_time=300,
        max_instances=1,
    )
    _scheduler.start()
    logger.info(f"APScheduler started (every {interval} min).")
    atexit.register(lambda: _scheduler.shutdown(wait=False))
