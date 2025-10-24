# Car Insurance API (Django + DRF)

A backend REST API for managing car owners, vehicles, insurance policies, and claims. Includes automatic detection of expired policies and a full event history per vehicle.

###  Features
- Create owners, cars, insurance policies, and claims
- Validate insurance by date
- View full history of a car (policies + claims)
- Automatic logging of expired policies
- Structured logging to file
- Test coverage ≥ 85%

---

##  Tech Stack

- Python 3.11+
- Django 5.x + Django REST Framework
- PostgreSQL (SQLite for dev/testing)
- APScheduler (background jobs)
- pytest
- Structured logging (to file)

---

##  Run Locally

```bash
# create env and install deps
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# migrate DB and start server
python manage.py migrate
python manage.py runserver

```
## API Endpoints

GET /health

Returns:
```bash
{ "status": "ok" }
```

POST /api/owners/

Request Body:
```bash
{ "name": string, "email": string }
```
Response:
```bash
{ "id": int, "name": string, "email": string }
```
POST /api/cars/

Request Body:
```bash
{
  "vin": string,
  "make": string,
  "model": string,
  "year_of_manufacture": int,
  "ownerId": int
}
```
Response:
```bash
{ "id": int, "vin": string, "make": string, "model": string, "year_of_manufacture": int, "ownerId": int }
```

POST /api/cars/{carId}/policies

Request Body:
```bash
{ "provider": string, "start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD" }
```

Response:
```bash
{ "id": int, "carId": int, "provider": string, "startDate": "YYYY-MM-DD", "endDate": "YYYY-MM-DD" }
```

GET /api/cars/{carId}/insurance-valid?date=YYYY-MM-DD

Response:
```bash
{ "carId": int, "date": "YYYY-MM-DD", "valid": boolean }
```
POST /api/cars/{carId}/claims

Request Body:
```bash
{ "claimDate": "YYYY-MM-DD", "description": string, "amount": float }
```

Response:
```bash
{
  "id": int, "carId": int, "claimDate": "YYYY-MM-DD",
  "description": string, "amount": string, "created_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

GET /api/cars/{carId}/history

Response:
```bash
[
  {
    "type": "POLICY",
    "policyId": int,
    "startDate": "YYYY-MM-DD",
    "endDate": "YYYY-MM-DD",
    "provider": string
  },
  {
    "type": "CLAIM",
    "claimId": int,
    "claimDate": "YYYY-MM-DD",
    "amount": float,
    "description": string
  }
]
```

## Testing

```bash
pytest
pytest --cov=. --cov-report=html
```

## Expired Policy Logging (Background Job)

Detects policies with end_date <= today and logged_expiry_at IS NULL

Log message format:

```bash
Policy {id} for car {carId} expired on {endDate}
```

## Project Structure
```bash
car_insurance/     # Django config
owners/            # owner API
cars/              # vehicle API
insurance/         # policies + expiry jobs
claims/            # insurance claims
history/           # full car history
core/              # scheduler setup
tests/             # pytest tests
```
## Validations & Rules
```bash
endDate >= startDate
Dates must be in ISO format (1900–2100)
Amounts must be positive and reasonable
Foreign keys enforced: owner, car
Policies cannot overlap
Each policy is logged only once after expiry
```
