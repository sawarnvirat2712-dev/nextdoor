from django.shortcuts import render
from .models import Place
from .utils import get_distance, get_open_status
from datetime import datetime
import pytz
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url="/accounts/login/")
def service_access(request, category):
    if request.user.is_authenticated:
        return redirect("place_list", category=category)

    return redirect(f"/accounts/login/?next=/services/{category}/")



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

        # 🔹 Parse inputs safely
        user_lat = float(lat)
        user_lng = float(lng)
        max_distance = float(distance)

        # 🔹 Current weekday in IST (Mon, Tue, ...)
        ist = pytz.timezone("Asia/Kolkata")
        today = datetime.now(ist).strftime("%a")  # e.g. "Mon"

        # 🔹 Fetch category places
        all_places = Place.objects.filter(category=category)

        for place in all_places:
            # 🔹 Skip if closed today
            if place.working_days and today not in place.working_days:
                continue

            # 🔹 Distance check
            dist = get_distance(
                user_lat,
                user_lng,
                float(place.latitude),
                float(place.longitude)
            )

            if dist <= max_distance:
                place.distance = round(dist, 2)

                # 🔹 OPEN / CLOSED / CLOSING SOON / 24H
                status, label = get_open_status(place)
                place.open_status = status       # open / closed / closing_soon / open_24
                place.open_label = label         # text label

                places.append(place)

    return render(request, "locations/place_list.html", {
        "places": places,
        "category": category
    })
