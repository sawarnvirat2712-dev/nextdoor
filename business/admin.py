from django.contrib import admin, messages
from .models import Business
from django.db import transaction

from locations.models import Place

CATEGORY_MAP = {
    'pg': 'pg',
    'mess': 'mess',
    'medical': 'medical',
    'stationery': 'stationery',
}


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):

    list_display = ("business_name", "category", "gstin", "is_approved")
    list_filter = ("is_approved", "category")
    search_fields = ("business_name", "gstin")

    actions = ["approve_business"]

    @admin.action(description="Approve selected businesses")
    def approve_business(self, request, queryset):
        created_count = 0
        failed = 0

        for business in queryset:

            # ⛔ Already approved
            if business.is_approved:
                continue

            # ❌ HARD VALIDATIONS (VERY IMPORTANT)
            if not business.phone:
                self.message_user(
                    request,
                    f"❌ {business.business_name}: Phone number missing",
                    messages.ERROR
                )
                failed += 1
                continue

            if not business.latitude or not business.longitude:
                self.message_user(
                    request,
                    f"❌ {business.business_name}: Location missing",
                    messages.ERROR
                )
                failed += 1
                continue

            try:
                # 🔒 TRANSACTION (ALL OR NOTHING)
                with transaction.atomic():
                    Place.objects.create(
                        name=business.business_name,
                        category=business.category,   # matches Place choices ✅
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
                    business.save(update_fields=["is_approved"])

                    created_count += 1

            except Exception as e:
                failed += 1
                self.message_user(
                    request,
                    f"❌ {business.business_name}: {str(e)}",
                    messages.ERROR
                )

        # ✅ FINAL MESSAGE
        self.message_user(
            request,
            f"✅ Added: {created_count} | ❌ Failed: {failed}",
            messages.SUCCESS if created_count else messages.WARNING
        )
