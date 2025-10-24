from django.urls import path
from .views import CarHistoryView

urlpatterns = [
    path("cars/<int:car_id>/history", CarHistoryView.as_view(), name="car-history"),
]