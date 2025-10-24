from rest_framework.generics import ListCreateAPIView
from .models import Car
from datetime import date
from .serializers import CarCreateSerializer, CarListSerializer
from django.shortcuts import get_object_or_404
from insurance.services import is_insured_on_date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CarListCreateView(ListCreateAPIView):
    queryset = Car.objects.select_related("owner").all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CarListSerializer
        return CarCreateSerializer
    
class InsuranceValidView(APIView):
    def get(self, request, car_id: int):
        get_object_or_404(Car, pk=car_id)

        date_str = request.query_params.get("date")
        if not date_str:
            return Response({"detail": "Query param 'date' is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            d = date.fromisoformat(date_str)
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        if d.year < 1900 or d.year > 2100:
            return Response({"detail": "Date out of allowed range (1900–2100)."}, status=status.HTTP_400_BAD_REQUEST)

        valid = is_insured_on_date(car_id, d)
        return Response({"carId": car_id, "date": d.isoformat(), "valid": valid}, status=status.HTTP_200_OK)