from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Business
from locations.models import Place,models


# =========================
# DASHBOARD
# =========================
@login_required(login_url="/accounts/login/")
def business_dashboard(request):
    business = get_object_or_404(Business, owner=request.user)

    place = getattr(business, "place", None)

    ratings = []
    avg_rating = 0
    total_ratings = 0

    if place:
        ratings = place.ratings.select_related("user")
        total_ratings = ratings.count()
        avg_rating = round(ratings.aggregate(models.Avg("rating"))["rating__avg"] or 0,1)

    return render(request, "business/business_dashboard.html", {
        "business": business,
        "place": place,
        "ratings": ratings,
        "avg_rating": avg_rating,
        "total_ratings": total_ratings,
    })



# =========================
# REGISTER BUSINESS
# =========================
@login_required

def register_business(request):
    business = Business.objects.filter(owner=request.user).first()

    # 1️⃣ No business → show form / create
    if not business:
        if request.method == "POST":
            business = Business.objects.create(
                owner=request.user,
                business_name=request.POST.get("business_name"),
                category=request.POST.get("category"),
                gstin=request.POST.get("gstin"),
                address=request.POST.get("address"),
                phone=request.POST.get("phone"),
                latitude=request.POST.get("latitude"),
                longitude=request.POST.get("longitude"),
                open_time=request.POST.get("open_time") or None,
                close_time=request.POST.get("close_time") or None,
                open_24_hours=bool(request.POST.get("open_24_hours")),
                working_days=request.POST.getlist("working_days"),
            )

            # 🔥 CREATE PLACE ONLY ONCE
            Place.objects.create(
                business=business,
                name=business.business_name,
                category=business.category,
                address=business.address,
                phone=business.phone,
                latitude=business.latitude,
                longitude=business.longitude,
                open_time=business.open_time,
                close_time=business.close_time,
                open_24_hours=business.open_24_hours,
                working_days=business.working_days,
            )

            return redirect("business_thank_you")

        return render(request, "business/register_business.html")

    # 2️⃣ Business exists but NOT approved
    if not business.is_approved:
        return render(request, "business/thank_you.html")

    # 3️⃣ Business approved → dashboard
    return redirect("business_dashboard")


def business_thank_you(request):
    return render(request, "business/thank_you.html")


# =========================
# EDIT BUSINESS
# =========================
@login_required

def edit_business(request):
    business = get_object_or_404(Business, owner=request.user)
    place = business.place  # ✅ OneToOne related_name works

    if request.method == "POST":
        # UPDATE BUSINESS
        business.business_name = request.POST["business_name"]
        business.phone = request.POST["phone"]
        business.address = request.POST["address"]
        business.save()

        # 🔥 SYNC PLACE
        place.name = business.business_name
        place.phone = business.phone
        place.address = business.address
        place.save()

        return redirect("business_dashboard")

    return render(request, "business/edit.html", {
        "business": business,
    })
