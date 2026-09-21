from typing import Optional
from datetime import datetime
from pydantic import BaseModel, UUID4

class AttendanceBase(BaseModel):
    student_id: UUID4
    bus_id: UUID4
    event_type: str # BOARD | OFFBOARD
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceResponse(AttendanceBase):
    id: UUID4
    event_timestamp: datetime
    confidence_score: Optional[float] = None
    verification_method: str
    device_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
