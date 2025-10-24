
from django.contrib import admin
from django.urls import path, include
from .health import health_ok 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/owners/", include("owners.urls")),
    path("api/cars/", include("cars.urls")),
    path("api/cars/", include("insurance.urls")),
    path("health", health_ok),
    path("api/cars/", include("claims.urls")),
    path("api/", include("history.urls")),
]
