from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.user import User, Parent, Driver
from app.models.student import Student
from app.models.fleet import Bus, Route, BusStop, BusAssignment
from app.models.attendance import Attendance
from app.models.face_profile import FaceProfile
from app.models.telemetry import GPSEvent, Alert, Notification

# Expose all models for Alembic autogenerate
__all__ = [
    "Base",
    "TimestampMixin",
    "User",
    "Parent",
    "Driver",
    "Student",
    "Bus",
    "Route",
    "BusStop",
    "BusAssignment",
    "Attendance",
    "FaceProfile",
    "GPSEvent",
    "Alert",
    "Notification",
]
