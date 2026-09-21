from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.models.base import TimestampMixin

class User(TimestampMixin, Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False) # ADMIN, PARENT, DRIVER
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    parent_profile = relationship("Parent", back_populates="user", uselist=False, cascade="all, delete-orphan")
    driver_profile = relationship("Driver", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class Parent(TimestampMixin, Base):
    __tablename__ = "parents"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    emergency_contact = Column(String, nullable=True)
    address = Column(String, nullable=True)

    user = relationship("User", back_populates="parent_profile")
    students = relationship("Student", back_populates="parent")


class Driver(TimestampMixin, Base):
    __tablename__ = "drivers"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    license_number = Column(String, unique=True, nullable=False)
    is_available = Column(Boolean, default=True)

    user = relationship("User", back_populates="driver_profile")
    buses = relationship("Bus", back_populates="current_driver")
