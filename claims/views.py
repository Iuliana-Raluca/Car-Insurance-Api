from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cars.models import Car
from .models import Claim
from .serializers import ClaimCreateSerializer
import logging

logger = logging.getLogger(__name__)
class CreateClaimView(APIView):
    def post (self, request, car_id: int):
        get_object_or_404(Car, pk=car_id)
        serializer = ClaimCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        claim = Claim.objects.create(
            car_id=car_id,
            **serializer.validated_data
        )
        header = {"Location": f"/api/cars/{car_id}/claims/{claim.id}"}
        logger.info(
            "Claim %s registered for car %s (date=%s, amount=%s)",
            claim.id, car_id, claim.claim_date, claim.amount
        )
        return Response(
            {
                "id": claim.id,
                "carId": car_id,
                "claimDate": claim.created_at.isoformat(),
                "description": claim.description,
                "amount": str(claim.amount),
                "created_at": claim.created_at.isoformat().replace("+00:00", "Z"),
            },
            status=status.HTTP_201_CREATED,
            headers=header
        )


