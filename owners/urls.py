from django.urls import path
from .views import OwnerCreateView

urlpatterns = [
    path("", OwnerCreateView.as_view(), name="owner-create"),
]
