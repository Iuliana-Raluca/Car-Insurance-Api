# insurance/jobs.py
from datetime import timedelta, timezone
import logging

from django.conf import settings
from django.db import transaction
from django.utils import timezone as dj_tz

from .models import InsurancePolicy

logger = logging.getLogger(__name__)

def _within_first_hour_local(now):
    """True dacă suntem în fereastra [00:00, 01:00) în TZ local."""
    local_now = dj_tz.localtime(now)
    start = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=1)
    return start <= local_now < end

def log_expired_policies_once():
    now = dj_tz.now()
    local_now = dj_tz.localtime(now)
    first_hour_only = getattr(settings, "SCHEDULER_FIRST_HOUR_ONLY", True)

    if first_hour_only and not _within_first_hour_local(now):
        logger.info("[expiry-job] outside first-hour window, skipping run")
        return

    today_local = dj_tz.localdate(now)

    processed = 0
    with transaction.atomic():
        qs = (
            InsurancePolicy.objects
            .select_for_update(skip_locked=True)
            .filter(logged_expiry_at__isnull=True, end_date=today_local)
        )
        to_process = list(qs) 
        if not to_process:
            logger.info("[expiry-job] no policies to log for end_date=%s", today_local)

        for p in to_process:
            logger.info("Policy %s for car %s expired on %s", p.id, p.car_id, p.end_date)
            p.logged_expiry_at = now.astimezone(timezone.utc)
            p.save(update_fields=["logged_expiry_at"])
            processed += 1

    logger.info("[expiry-job] processed=%d end_date=%s", processed, today_local)
