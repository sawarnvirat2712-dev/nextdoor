from django.urls import path
from .views import service_access, place_list

urlpatterns = [
    path("services/<str:category>/", service_access, name="service_access"),
    path("<str:category>/", place_list, name="place_list"),
]
