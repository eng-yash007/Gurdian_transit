from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Float, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base
from app.models.base import TimestampMixin

class Bus(TimestampMixin, Base):
    __tablename__ = "buses"

    bus_number = Column(String, unique=True, index=True, nullable=False)
    license_plate = Column(String, unique=True, nullable=False)
    capacity = Column(Integer, nullable=False, default=40)
    current_driver_id = Column(UUID(as_uuid=True), ForeignKey("drivers.id", ondelete="SET NULL"), nullable=True)
    status = Column(String, default="ACTIVE") # ACTIVE | INACTIVE | MAINTENANCE

    current_driver = relationship("Driver", back_populates="buses")
    bus_assignments = relationship("BusAssignment", back_populates="bus")
    gps_events = relationship("GPSEvent", back_populates="bus")
    alerts = relationship("Alert", back_populates="bus")
    attendance_records = relationship("Attendance", back_populates="bus")


class Route(TimestampMixin, Base):
    __tablename__ = "routes"

    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    waypoints = Column(JSONB, nullable=True)
    start_point = Column(String, nullable=True)
    end_point = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    stops = relationship("BusStop", back_populates="route", cascade="all, delete-orphan")
    bus_assignments = relationship("BusAssignment", back_populates="route")


class BusStop(TimestampMixin, Base):
    __tablename__ = "bus_stops"

    route_id = Column(UUID(as_uuid=True), ForeignKey("routes.id", ondelete="CASCADE"), nullable=False)
    stop_name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    sequence_order = Column(Integer, nullable=False)
    scheduled_time = Column(Time, nullable=True)

    route = relationship("Route", back_populates="stops")
    pickup_assignments = relationship("BusAssignment", foreign_keys="[BusAssignment.pickup_stop_id]", back_populates="pickup_stop")
    dropoff_assignments = relationship("BusAssignment", foreign_keys="[BusAssignment.dropoff_stop_id]", back_populates="dropoff_stop")


class BusAssignment(TimestampMixin, Base):
    __tablename__ = "bus_assignments"

    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    bus_id = Column(UUID(as_uuid=True), ForeignKey("buses.id", ondelete="CASCADE"), nullable=False)
    route_id = Column(UUID(as_uuid=True), ForeignKey("routes.id", ondelete="CASCADE"), nullable=False)
    pickup_stop_id = Column(UUID(as_uuid=True), ForeignKey("bus_stops.id", ondelete="SET NULL"), nullable=True)
    dropoff_stop_id = Column(UUID(as_uuid=True), ForeignKey("bus_stops.id", ondelete="SET NULL"), nullable=True)
    academic_year = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    student = relationship("Student", back_populates="bus_assignments")
    bus = relationship("Bus", back_populates="bus_assignments")
    route = relationship("Route", back_populates="bus_assignments")
    pickup_stop = relationship("BusStop", foreign_keys=[pickup_stop_id], back_populates="pickup_assignments")
    dropoff_stop = relationship("BusStop", foreign_keys=[dropoff_stop_id], back_populates="dropoff_assignments")
