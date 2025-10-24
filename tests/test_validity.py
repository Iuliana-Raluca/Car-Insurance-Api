import pytest
from tests.factories import CarFactory
from insurance.models import InsurancePolicy

@pytest.mark.django_db
def test_validity_true_false(api_client):
    car = CarFactory()
    InsurancePolicy.objects.create(
        car=car, provider="ACME", start_date="2025-01-01", end_date="2025-12-31"
    )
    # true inside window
    r1 = api_client.get(f"/api/cars/{car.id}/insurance-valid?date=2025-06-01")
    assert r1.status_code == 200
    assert r1.json()["valid"] is True
    # false outside
    r2 = api_client.get(f"/api/cars/{car.id}/insurance-valid?date=2026-01-01")
    assert r2.status_code == 200
    assert r2.json()["valid"] is False

@pytest.mark.django_db
def test_validity_404_car(api_client):
    r = api_client.get("/api/cars/999999/insurance-valid?date=2025-06-01")
    assert r.status_code == 404

@pytest.mark.django_db
def test_validity_400_bad_date(api_client):
    car = CarFactory()
    r1 = api_client.get(f"/api/cars/{car.id}/insurance-valid")  # missing
    assert r1.status_code == 400
    r2 = api_client.get(f"/api/cars/{car.id}/insurance-valid?date=06-01-2025")  # wrong format
    assert r2.status_code == 400
    r3 = api_client.get(f"/api/cars/{car.id}/insurance-valid?date=1800-01-01")  # out of range
    assert r3.status_code == 400
