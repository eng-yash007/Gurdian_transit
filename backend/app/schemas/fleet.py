from typing import Optional, List, Any
from datetime import time, datetime
from pydantic import BaseModel, UUID4

# --- Bus ---
class BusBase(BaseModel):
    bus_number: str
    license_plate: str
    capacity: int
    status: str

class BusResponse(BusBase):
    id: UUID4
    current_driver_id: Optional[UUID4] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# --- Route ---
class RouteBase(BaseModel):
    name: str
    description: Optional[str] = None
    waypoints: Optional[Any] = None
    start_point: Optional[str] = None
    end_point: Optional[str] = None
    is_active: bool

class RouteResponse(RouteBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# --- BusStop ---
class BusStopBase(BaseModel):
    stop_name: str
    latitude: float
    longitude: float
    sequence_order: int
    scheduled_time: Optional[time] = None

class BusStopResponse(BusStopBase):
    id: UUID4
    route_id: UUID4
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
