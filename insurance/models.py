from django.db import models
from cars.models import Car

class InsurancePolicy(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="policies")
    provider = models.CharField(max_length=128, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    logged_expiry_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["car", "start_date", "end_date"]),
        ]

    def __str__(self):
        return f"Policy {self.id} - car {self.car_id} ({self.start_date}..{self.end_date})"
