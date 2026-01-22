# business/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_business, name="register_business"),
    path("dashboard/", views.business_dashboard, name="business_dashboard"),
    path("dashboard/edit/", views.edit_business, name="edit_business"),
    path("thank-you/", views.business_thank_you, name="business_thank_you"),

]
