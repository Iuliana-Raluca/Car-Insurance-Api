from django.db import models

class Owner(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.id})"