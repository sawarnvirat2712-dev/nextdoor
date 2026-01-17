from django.shortcuts import render
from .models import Place
from .utils import get_distance


def place_list(request, category):
    places = []
    if request.method == "POST":
        lat = request.POST.get("lat")
        lng = request.POST.get("lng")
        distance = request.POST.get("distance")

        if not lat or not lng or not distance:
            return render(request, "locations/place_list.html", {
                "places": [],
                "category": category,
                "error": "Location not available. Please allow location access."
            })

        user_lat = float(lat)
        user_lng = float(lng)
        max_distance = float(distance)

        max_distance = float(request.POST.get("distance"))

        all_places = Place.objects.filter(category=category)

        for place in all_places:
            dist = get_distance(
                user_lat, user_lng,
                float(place.latitude), float(place.longitude)
            )
            if dist <= max_distance:
                place.distance = round(dist, 2)
                places.append(place)

    return render(request, "locations/place_list.html", {
        "places": places,
        "category": category
    })
