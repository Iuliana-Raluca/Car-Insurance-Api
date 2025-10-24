import pytest
from tests.factories import CarFactory
from insurance.models import InsurancePolicy
from claims.models import Claim

@pytest.mark.django_db
def test_history_ordering_and_shape(api_client):
    car = CarFactory()
    InsurancePolicy.objects.create(car=car, provider="AXA", start_date="2025-01-01", end_date="2025-03-01")
    Claim.objects.create(car=car, claim_date="2025-02-15", description="scratch", amount="50.00")

    r = api_client.get(f"/api/cars/{car.id}/history")
    assert r.status_code == 200
    events = r.json()
    # sorted ascending by date string
    dates = [e.get("startDate") or e.get("claimDate") for e in events]
    assert dates == sorted(dates)
    # minimal shape checks
    assert any(e["type"] == "POLICY" for e in events)
    assert any(e["type"] == "CLAIM" for e in events)
