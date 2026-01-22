from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Place(models.Model):

    CATEGORY_CHOICES = [
        ('pg', 'PG / Hostel'),
        ('mess', 'Mess / Tiffin'),
        ('medical', 'Medical Store'),
        ('stationery', 'Stationery'),
    ]

    WEEK_DAYS = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]

    # 🔹 BASIC INFO
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )

    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)

    # 🔹 BUSINESS TIMING
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    open_24_hours = models.BooleanField(default=False)

    # 🔹 WORKING DAYS (Mon–Sun)
    working_days = models.JSONField(
        default=list,
        help_text="Example: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']"
    )

    # 🔹 STATUS
    is_verified = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["is_verified"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    def is_working_today(self, today):
        """
        today: 'Mon', 'Tue', ...
        """
        return not self.working_days or today in self.working_days



class Rating(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    value = models.PositiveSmallIntegerField()  # 1–5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.value}⭐ for {self.place.name}"
