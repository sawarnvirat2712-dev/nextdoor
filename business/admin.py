from django.contrib import admin
from .models import Business
from locations.models import Place


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):

    list_display = ("business_name", "category", "gstin", "is_approved")
    list_filter = ("is_approved", "category")
    search_fields = ("business_name", "gstin")

    actions = ["approve_business"]

    def approve_business(self, request, queryset):
        for business in queryset:
            if business.is_approved:
                continue

            Place.objects.create(
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
                is_verified=True,
            )

            business.is_approved = True
            business.save()

    approve_business.short_description = "Approve selected businesses"
