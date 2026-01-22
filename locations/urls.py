from django.urls import path
from . import views 

urlpatterns = [
    path("services/<str:category>/", views.service_access, name="service_access"),
    path("<str:category>/", views.place_list, name="place_list"),
    path("place/<int:place_id>/", views.place_detail, name="place_detail"),
    path("place/<int:place_id>/rate/", views.submit_rating, name="submit_rating"),

]
