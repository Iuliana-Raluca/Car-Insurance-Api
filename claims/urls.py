from django.urls import path
from .views import CreateClaimView

urlpatterns = [path("<int:car_id>/claims", CreateClaimView.as_view(), name="claim-create")]
