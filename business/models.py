from django.db import models
from django.contrib.auth.models import User


class Business(models.Model):

    CATEGORY_CHOICES = [
        ('pg', 'PG / Hostel'),
        ('mess', 'Mess / Tiffin'),
        ('medical', 'Medical Store'),
        ('stationery', 'Stationery'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    business_name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    gstin = models.CharField(max_length=15)

    address = models.TextField()
    phone = models.CharField(max_length=15)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    # 🔹 TIMINGS
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    open_24_hours = models.BooleanField(default=False)
    working_days = models.JSONField(default=list)

    # 🔥 REQUIRED FOR ADMIN
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
