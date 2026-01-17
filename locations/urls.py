from django.urls import path
from .views import place_list

urlpatterns = [
    path("<str:category>/", place_list, name="place_list"),
]
