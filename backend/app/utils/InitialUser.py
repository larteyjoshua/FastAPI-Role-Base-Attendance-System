from random import seed
from app.utils.config import settings
class User:
    """
    Constants for the various roles scoped in the application ecosystem
    """

    SUPER_ADMIN = {
        "name": "SUPERADMIN",
        "email": settings.FIRST_SUPER_ADMIN_EMAIL,
        "password": settings.FIRST_SUPER_ADMIN_PASSWORD,
        "location": settings.LOCATION,
        "gpsAddress":settings.ADDRESS

    }
    