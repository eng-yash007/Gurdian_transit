from sqlalchemy import Column, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.models.base import TimestampMixin

class Student(TimestampMixin, Base):
    __tablename__ = "students"

    parent_id = Column(UUID(as_uuid=True), ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    student_id_number = Column(String, unique=True, index=True, nullable=False)
    grade = Column(String, nullable=True)
    section = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    photo_url = Column(String, nullable=True)
    current_status = Column(String, default="OFF_BOARD") # OFF_BOARD | ON_BOARD | ABSENT
    is_active = Column(Boolean, default=True)

    parent = relationship("Parent", back_populates="students")
    bus_assignments = relationship("BusAssignment", back_populates="student", cascade="all, delete-orphan")
    face_profiles = relationship("FaceProfile", back_populates="student", cascade="all, delete-orphan")
    attendance_records = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="student", cascade="all, delete-orphan")
