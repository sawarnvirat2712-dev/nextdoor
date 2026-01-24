from django.core.management.base import BaseCommand
from locations.models import Place
import random
import math

CENTER_LAT = 25.490482870160793
CENTER_LNG = 81.86327333593526

CATEGORIES = ["pg", "mess", "medical", "stationery"]

def generate_nearby_point(lat, lng, radius_km):
    """
    Generate a random point within radius_km of (lat, lng)
    """
    radius_in_degrees = radius_km / 111  # approx conversion

    u = random.random()
    v = random.random()

    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v

    delta_lat = w * math.cos(t)
    delta_lng = w * math.sin(t) / math.cos(math.radians(lat))

    return lat + delta_lat, lng + delta_lng


class Command(BaseCommand):
    help = "Seed 50 fake places around a fixed location"

    def handle(self, *args, **kwargs):
        Place.objects.all().delete()

        places = []

        for i in range(50):
            radius = random.uniform(0.2, 8)  # 0.2km to 8km
            lat, lng = generate_nearby_point(CENTER_LAT, CENTER_LNG, radius)

            place = Place(
                name=f"Demo Place {i+1}",
                category=random.choice(CATEGORIES),
                latitude=round(lat, 6),
                longitude=round(lng, 6),
                address=f"Test Address {i+1}, Nearby Area",
                phone=f"9{random.randint(100000000, 999999999)}",
                open_24_hours=random.choice([True, False]),
                working_days=["Mon", "Tue", "Wed", "Thu", "Fri"],
                is_verified=True,
            )
            places.append(place)

        Place.objects.bulk_create(places)

        self.stdout.write(
            self.style.SUCCESS("✅ Successfully seeded 50 fake places")
        )
