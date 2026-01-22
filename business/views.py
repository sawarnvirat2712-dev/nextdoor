from django.shortcuts import render, redirect
from .models import Business

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from locations.models import Place


@login_required
def business_dashboard(request):
    business = Business.objects.get(owner=request.user)
    return render(request, "business/business_dashboard.html", {
        "business": business,
    })


def register_business(request):
    business = Business.objects.filter(owner=request.user).first()

    # 1️⃣ No business → show registration form
    if not business:
        if request.method == "POST":
            Business.objects.create(
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
            return redirect("business_thank_you")

        return render(request, "business/register_business.html")

    # 2️⃣ Business exists but NOT approved
    if not business.is_approved:
        return render(request, "business/thank_you.html")

    # 3️⃣ Business approved → DASHBOARD (✅ FIX)
    return redirect("business_dashboard")

def business_thank_you(request):
    return render(request, "business/thank_you.html")


@login_required
def edit_business(request):
    business = Business.objects.get(owner=request.user)

    if request.method == "POST":
        business.business_name = request.POST.get("business_name")
        business.phone = request.POST.get("phone")
        business.address = request.POST.get("address")
        business.save()
        return redirect("business_dashboard")

    return render(request, "business/edit_business.html", {
        "business": business
    })


