from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import UUID4

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.attendance import Attendance
from app.models.student import Student
from app.schemas.attendance import AttendanceCreate, AttendanceResponse

router = APIRouter()

@router.get("/student/{student_id}", response_model=List[AttendanceResponse])
async def read_student_attendance(
    student_id: UUID4,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve attendance history for a specific student.
    """
    # Verify student exists and parent authorization
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    if current_user.role == "PARENT":
        if not current_user.parent_profile or student.parent_id != current_user.parent_profile.id:
            raise HTTPException(status_code=403, detail="Not authorized to view this student's attendance")
            
    # Fetch attendance
    result = await db.execute(
        select(Attendance)
        .where(Attendance.student_id == student_id)
        .order_by(Attendance.event_timestamp.desc())
    )
    attendance_records = result.scalars().all()
    return attendance_records


@router.post("/manual", response_model=AttendanceResponse)
async def create_manual_attendance(
    *,
    db: AsyncSession = Depends(get_db),
    attendance_in: AttendanceCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create a manual attendance event. 
    This acts as a mock for our future AI-based computer vision events.
    """
    # Anyone authenticated can push a manual event for now (MVP testing)
    
    # Verify student exists
    result = await db.execute(select(Student).where(Student.id == attendance_in.student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    attendance = Attendance(
        student_id=attendance_in.student_id,
        bus_id=attendance_in.bus_id,
        event_type=attendance_in.event_type,
        verification_method="MANUAL_OVERRIDE", # Mock event
        latitude=attendance_in.latitude,
        longitude=attendance_in.longitude
    )
    
    # Update current status on student record
    student.current_status = attendance_in.event_type
    
    db.add(attendance)
    await db.commit()
    await db.refresh(attendance)
    
    return attendance
