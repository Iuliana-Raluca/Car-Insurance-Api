import pytest
from freezegun import freeze_time
from django.utils import timezone as dj_tz
from tests.factories import CarFactory, PolicyFactory
from insurance.jobs import log_expired_policies_once

@pytest.mark.django_db
def test_scheduler_marks_and_logs_expired_policies(caplog, settings):
    settings.SCHEDULER_FIRST_HOUR_ONLY = False

    car = CarFactory()
    # end_date == today (2025-10-22 în test)
    with freeze_time("2025-10-22 10:00:00"):
        PolicyFactory(car=car, provider="ACME", start_date="2025-01-01", end_date="2025-10-22")
        caplog.clear()
        log_expired_policies_once()  
        assert any("expired on 2025-10-22" in rec.message for rec in caplog.records)
        prev = list(caplog.records)
        caplog.clear()
        log_expired_policies_once()
        assert not any("expired on 2025-10-22" in rec.message for rec in caplog.records)
