from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from cars.models import Car
from .models import InsurancePolicy
from .serializers import InsurancePolicyCreateSerializer
import logging

logger = logging.getLogger(__name__) 

class CreatePolicyView(APIView):
    def post(self, request, car_id: int):
        get_object_or_404(Car, pk=car_id)

        serializer = InsurancePolicyCreateSerializer(
            data=request.data,
            context={"car_id": car_id}  
        )
        serializer.is_valid(raise_exception=True)

        policy = InsurancePolicy.objects.create(
            car_id=car_id,
            **serializer.validated_data
        )
        logger.info(
            "Policy %s created for car %s (provider=%s, start=%s, end=%s)",
            policy.id, car_id, policy.provider, policy.start_date, policy.end_date
        )
        return Response(
            {
                "id": policy.id,
                "carId": car_id,
                "provider": policy.provider,
                "startDate": policy.start_date.isoformat(),
                "endDate": policy.end_date.isoformat(),
            },
            status=status.HTTP_201_CREATED
        )
        