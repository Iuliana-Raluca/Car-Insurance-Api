import pytest
from tests.factories import CarFactory

@pytest.mark.django_db
def test_create_claim_201_with_location(api_client):
    car = CarFactory()
    payload = {"claimDate": "2025-06-10", "description": "Rear bumper", "amount": 123.45}
    resp = api_client.post(f"/api/cars/{car.id}/claims", payload, format="json")
    assert resp.status_code == 201
    assert "Location" in resp.headers
    data = resp.json()
    assert data["carId"] == car.id
    assert data["amount"] == "123.45"

@pytest.mark.django_db
def test_create_claim_400_validations(api_client):
    car = CarFactory()
    # amount <= 0
    r1 = api_client.post(f"/api/cars/{car.id}/claims", {"claimDate":"2025-06-10","description":"x","amount":0}, format="json")
    assert r1.status_code == 400
    # empty description
    r2 = api_client.post(f"/api/cars/{car.id}/claims", {"claimDate":"2025-06-10","description":" ","amount":10}, format="json")
    assert r2.status_code == 400
    # out-of-range date
    r3 = api_client.post(f"/api/cars/{car.id}/claims", {"claimDate":"1800-01-01","description":"x","amount":10}, format="json")
    assert r3.status_code == 400

@pytest.mark.django_db
def test_create_claim_404_car(api_client):
    resp = api_client.post("/api/cars/999999/claims", {"claimDate":"2025-06-10","description":"x","amount":10}, format="json")
    assert resp.status_code == 404
