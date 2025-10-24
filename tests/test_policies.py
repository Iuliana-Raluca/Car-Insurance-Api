import datetime as dt
import pytest
from tests.factories import CarFactory

@pytest.mark.django_db
def test_create_policy_201(api_client):
    car = CarFactory()
    payload = {
        "provider": "AXA",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31"
    }
    resp = api_client.post(f"/api/cars/{car.id}/policies", payload, format="json")
    assert resp.status_code == 201
    body = resp.json()
    assert body["carId"] == car.id
    assert body["startDate"] == "2025-01-01"
    assert body["endDate"] == "2025-12-31"

@pytest.mark.django_db
def test_create_policy_400_end_before_start(api_client):
    car = CarFactory()
    payload = {
        "provider": "AXA",
        "start_date": "2025-12-31",
        "end_date": "2025-01-01"
    }
    resp = api_client.post(f"/api/cars/{car.id}/policies", payload, format="json")
    assert resp.status_code == 400
    assert "endDate must not precede startDate" in str(resp.content)

@pytest.mark.django_db
def test_create_policy_400_overlap(api_client):
    car = CarFactory()
    # existing policy
    api_client.post(f"/api/cars/{car.id}/policies", {
        "provider": "AXA",
        "start_date": "2025-01-01",
        "end_date": "2025-01-31"
    }, format="json")
    # overlapping
    resp = api_client.post(f"/api/cars/{car.id}/policies", {
        "provider": "AXA",
        "start_date": "2025-01-15",
        "end_date": "2025-02-01"
    }, format="json")
    assert resp.status_code == 400
    assert "Overlapping policy" in str(resp.content)

@pytest.mark.django_db
def test_create_policy_404_car_not_found(api_client):
    resp = api_client.post("/api/cars/999999/policies", {
        "provider": "AXA",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31"
    }, format="json")
    assert resp.status_code == 404
