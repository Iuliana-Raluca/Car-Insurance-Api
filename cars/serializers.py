
from datetime import date
from rest_framework import serializers
from .models import Car
from owners.models import Owner
from owners.serializers import OwnerSerializer 

class CarCreateSerializer(serializers.ModelSerializer):
    ownerId = serializers.IntegerField(write_only=True)

    class Meta:
        model = Car
        fields = ["id", "vin", "make", "model", "year_of_manufacture", "ownerId"]

    def validate_vin(self, v):
        v = (v or "").strip()
        if not v:
            raise serializers.ValidationError("VIN is required.")
        if len(v) > 32:
            raise serializers.ValidationError("VIN too long (max 32).")
        return v

    def validate_year_of_manufacture(self, y):
        current = date.today().year
        if y < 1900 or y > current + 1:
            raise serializers.ValidationError(f"Year must be between 1900 and {current+1}.")
        return y

    def validate_ownerId(self, oid):
        if not Owner.objects.filter(id=oid).exists():
            raise serializers.ValidationError("Owner not found.")
        return oid

    def create(self, validated):
        owner_id = validated.pop("ownerId")
        return Car.objects.create(owner_id=owner_id, **validated)


class CarListSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    yearOfManufacture = serializers.IntegerField(source="year_of_manufacture")

    class Meta:
        model = Car
        fields = ["id", "vin", "make", "model", "yearOfManufacture", "owner"]
