from django.shortcuts import render
from .models import Place

def place_list(request, category):
    places = Place.objects.filter(category=category)
    return render(request, "locations/place_list.html", {
        "places": places,
        "category": category
    })
