from django.db import models
from cars.models import Car

class Claim(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="claims")
    claim_date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["car", "claim_date"]),
        ]

    def __str__(self):
        return f"Claim {self.id} - car {self.car_id} ({self.claim_date})"