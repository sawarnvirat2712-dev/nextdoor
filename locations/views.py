from django.shortcuts import render
from .models import Place
from .utils import get_distance, get_open_status
from datetime import datetime
import pytz
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from .models import Place, Rating
from .utils import get_open_status

from django.contrib import messages


@login_required

def service_access(request, category):
    if request.user.is_authenticated:
        return redirect("place_list", category=category)

    return redirect(f"/accounts/login/?next=/services/{category}/")


@login_required

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


@login_required

def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    avg_rating = place.ratings.aggregate(avg=Avg("rating"))["avg"] or 0
    total_ratings = place.ratings.count()

    user_has_rated = False
    if request.user.is_authenticated:
        user_has_rated = place.ratings.filter(user=request.user).exists()

    context = {
        "place": place,
        "avg_rating": round(avg_rating, 1),
        "total_ratings": total_ratings,
        "user_has_rated": user_has_rated,
    }

    return render(request, "locations/place_detail.html", context)


@login_required
def submit_rating(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    if request.method == "POST":
        rating_value = int(request.POST.get("rating"))

        rating_obj, created = Rating.objects.update_or_create(
            user=request.user,
            place=place,
            defaults={"rating": rating_value}
        )

    return redirect("place_detail", place_id=place.id)
