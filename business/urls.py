from django.urls import path
from .views import register_business

urlpatterns = [
    path("register/", register_business, name="register_business"),
]
