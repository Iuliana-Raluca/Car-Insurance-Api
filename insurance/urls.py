from django.urls import path
from .views import CreatePolicyView

urlpatterns = [
    path("<int:car_id>/policies", CreatePolicyView.as_view(), name="policy-create"),
]
