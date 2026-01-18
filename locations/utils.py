from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta
import pytz

IST = pytz.timezone("Asia/Kolkata")

def get_open_status(place):
    """
    Returns: (status, label)
    status: open | closed | closing_soon | open_24
    """

    if place.open_24_hours:
        return "open_24", "Open 24 Hours"

    if not place.open_time or not place.close_time:
        return "closed", "Closed"

    now = datetime.now(IST).time()

    # Closed
    if now < place.open_time or now > place.close_time:
        return "closed", "Closed"

    # Closing soon (within 30 mins)
    close_dt = datetime.combine(datetime.today(), place.close_time)
    now_dt = datetime.combine(datetime.today(), now)

    if close_dt - now_dt <= timedelta(minutes=30):
        return "closing_soon", "Closing Soon"

    return "open", "Open"

def get_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c
