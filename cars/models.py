from django.db import models
from owners.models import Owner

class Car(models.Model):
    vin = models.CharField(max_length=32, unique=True)  
    make = models.CharField(max_length=64, null=True, blank=True)
    model = models.CharField(max_length=64, null=True, blank=True)
    year_of_manufacture = models.PositiveIntegerField()  
    owner = models.ForeignKey(
        Owner,
        on_delete=models.PROTECT,  
        related_name="cars"
    )

    class Meta:
        indexes = [models.Index(fields=["vin"])]

    def __str__(self):
        return f"{self.vin}"
