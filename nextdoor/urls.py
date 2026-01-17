from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("services/", include("services.urls")),  # 👈 DASHBOARD APP
    path("", include("users.urls")), 
    path("locations/", include("locations.urls")),
]
