from django.db import models

class Place(models.Model):

    CATEGORY_CHOICES=[
        ('pg','PG/Hostel'),
        ('mess','Mess/Tiffin'),
        ('medical','Medical Store'),
        ('stationery','Stationery'),
    ]

    name=models.CharField(max_length=200)
    category=models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    latitude=models.DecimalField(max_digits=9,decimal_places=6)
    longitude=models.DecimalField(max_digits=9,decimal_places=6)

    address=models.TextField(blank=True)
    phone=models.CharField(max_length=15,blank=True)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"