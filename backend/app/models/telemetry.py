from sqlalchemy import Column, String, Boolean, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime, timezone
from app.core.database import Base
from app.models.base import TimestampMixin

class GPSEvent(TimestampMixin, Base):
    __tablename__ = "gps_events"

    bus_id = Column(UUID(as_uuid=True), ForeignKey("buses.id", ondelete="CASCADE"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed = Column(Float, nullable=True)
    heading = Column(Float, nullable=True)
    recorded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    bus = relationship("Bus", back_populates="gps_events")


class Alert(TimestampMixin, Base):
    __tablename__ = "alerts"

    alert_type = Column(String, nullable=False) # UNKNOWN_PERSON | ROUTE_DEVIATION | EMERGENCY | DEVICE_OFFLINE
    severity = Column(String, nullable=False) # LOW | MEDIUM | HIGH | CRITICAL
    status = Column(String, default="OPEN") # OPEN | ACKNOWLEDGED | RESOLVED
    bus_id = Column(UUID(as_uuid=True), ForeignKey("buses.id", ondelete="SET NULL"), nullable=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="SET NULL"), nullable=True)
    description = Column(String, nullable=True)
    metadata_json = Column(JSONB, nullable=True)

    bus = relationship("Bus", back_populates="alerts")
    student = relationship("Student", back_populates="alerts")


class Notification(TimestampMixin, Base):
    __tablename__ = "notifications"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    notification_type = Column(String, nullable=False) # ATTENDANCE | LOCATION | SAFETY | SYSTEM
    is_read = Column(Boolean, default=False)

    user = relationship("User", back_populates="notifications")
