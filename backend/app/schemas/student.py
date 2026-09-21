from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, UUID4

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    student_id_number: str
    grade: Optional[str] = None
    section: Optional[str] = None
    date_of_birth: Optional[date] = None
    photo_url: Optional[str] = None
    current_status: str
    is_active: bool

class StudentResponse(StudentBase):
    id: UUID4
    parent_id: UUID4
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
