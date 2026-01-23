from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from business.models import Business

class Place(models.Model):
    business = models.OneToOneField(
        Business,
        on_delete=models.CASCADE,
        related_name="place"
    )

    CATEGORY_CHOICES = [
        ('pg', 'PG / Hostel'),
        ('mess', 'Mess / Tiffin'),
        ('medical', 'Medical Store'),
        ('stationery', 'Stationery'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)

    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    open_24_hours = models.BooleanField(default=False)

    working_days = models.JSONField(default=list)

    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    rating = models.IntegerField()

    class Meta:
        unique_together = ("user", "place")
