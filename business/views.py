from django.shortcuts import render, redirect
from .models import Business

def register_business(request):
    if request.method == "POST":
        Business.objects.create(
            business_name=request.POST.get("business_name"),
            category=request.POST.get("category"),
            gstin=request.POST.get("gstin"),

            open_time=request.POST.get("open_time") or None,
            close_time=request.POST.get("close_time") or None,
            open_24_hours=bool(request.POST.get("open_24_hours")),

            working_days=request.POST.getlist("working_days"),
            address = request.POST.get("address"),
            latitude=request.POST.get("latitude"),
            longitude=request.POST.get("longitude"),
        )
        return redirect("register_business")  # or success page

    return render(request, "business/register_business.html")
