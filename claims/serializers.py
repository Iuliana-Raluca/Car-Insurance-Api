from rest_framework import serializers
from .models import Claim

class ClaimCreateSerializer(serializers.ModelSerializer):
    claimDate = serializers.DateField(source="claim_date")
    description = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = Claim
        fields = ["id" , "claimDate" , "description" , "amount", "created_at"]
        read_fields = ["id", "created_at"]

    def validate_claimDate(self, d):
        if d.year < 1900 or d.year > 2100:
            raise serializers.ValidationError("Date out of allowed range 1900–2100.")
        return d
    def validate_description(self, v):
        if not v or not v.strip():
            raise serializers.ValidationError("Description is required.")
        return v
    def validate_amount(self, v):
        if v is None or v <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        if v >= 1_000_000:
            raise serializers.ValidationError("Amount too large.")
        return v
    