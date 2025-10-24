from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cars.models import Car
from insurance.models import InsurancePolicy
from claims.models import Claim

class CarHistoryView(APIView):
    def get(self, request, car_id: int):
        get_object_or_404(Car, pk=car_id)

        policies = InsurancePolicy.objects.filter(car_id=car_id).values(
            "id", "provider", "start_date", "end_date"
        )
        claims = Claim.objects.filter(car_id=car_id).values(
            "id", "claim_date", "description", "amount"
        )

        events = []
        for p in policies:
            events.append({
                "type": "POLICY",
                "policyId": p["id"],
                "startDate": p["start_date"].isoformat(),
                "endDate": p["end_date"].isoformat(),
                "provider": p["provider"],
            })
        for c in claims:
            events.append({
                "type": "CLAIM",
                "claimId": c["id"],
                "claimDate": c["claim_date"].isoformat(),
                "description": c["description"],
                "amount": float(c["amount"]),
            })

        def event_date(e):
            return e.get("startDate") or e.get("claimDate")

        events.sort(key=event_date)  

        return Response(events)
