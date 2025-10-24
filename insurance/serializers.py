from datetime import date
from rest_framework import serializers
from .models import InsurancePolicy

def _validate_date_range(d: date):
    if d.year < 1900 or d.year > 2100:
        raise serializers.ValidationError("Date out of allowed range 1900–2100.")

class InsurancePolicyCreateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    class Meta:
        model = InsurancePolicy
        fields = ["id", "provider", "start_date", "end_date"]

    def validate(self, attrs):
        start = attrs["start_date"]
        end = attrs["end_date"]

        _validate_date_range(start)
        _validate_date_range(end)
        if end < start:
            raise serializers.ValidationError("endDate must not precede startDate.")

        car_id = self.context.get("car_id")
        if car_id is not None:
            overlaps = InsurancePolicy.objects.filter(
                car_id=car_id
            ).filter(
                start_date__lte=end,
                end_date__gte=start,
            )
            if overlaps.exists():
                raise serializers.ValidationError(
                    " Only one active policy may exist at any point in time."
                )
        return attrs
