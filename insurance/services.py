from datetime import date
from .models import InsurancePolicy

def is_insured_on_date(car_id: int, d: date) -> bool:
    return InsurancePolicy.objects.filter(
        car_id=car_id,
        start_date__lte=d,
        end_date__gte=d
    ).exists()
