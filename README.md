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
