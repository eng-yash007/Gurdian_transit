from sqlalchemy import Column, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.core.database import Base
from app.models.base import TimestampMixin

class Attendance(TimestampMixin, Base):
    __tablename__ = "attendance"

    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    bus_id = Column(UUID(as_uuid=True), ForeignKey("buses.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String, nullable=False) # BOARD | OFFBOARD | ABSENT | MANUAL
    event_timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    confidence_score = Column(Float, nullable=True) # AI confidence score
    verification_method = Column(String, default="MANUAL_OVERRIDE") # AI_FACE | MANUAL_OVERRIDE | NFC
    device_id = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    student = relationship("Student", back_populates="attendance_records")
    bus = relationship("Bus", back_populates="attendance_records")
