from django.urls import path
from .views import CarListCreateView,InsuranceValidView

urlpatterns = [
    path("", CarListCreateView.as_view(), name="car-list-create"),
    path("<int:car_id>/insurance-valid", InsuranceValidView.as_view(), name="insurance-valid"),
]
