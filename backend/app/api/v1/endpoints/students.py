from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import UUID4

from app.core.database import get_db
from app.api.deps import get_current_parent_user, get_current_user
from app.models.user import User
from app.models.student import Student
from app.schemas.student import StudentResponse

router = APIRouter()

@router.get("/me", response_model=List[StudentResponse])
async def read_my_students(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_parent_user),
) -> Any:
    """
    Retrieve students associated with the currently logged in parent.
    """
    if not current_user.parent_profile:
        raise HTTPException(status_code=404, detail="Parent profile not found")
        
    result = await db.execute(
        select(Student).where(Student.parent_id == current_user.parent_profile.id)
    )
    students = result.scalars().all()
    return students


@router.get("/{student_id}", response_model=StudentResponse)
async def read_student(
    student_id: UUID4,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get specific student details by ID.
    """
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    # Security: Ensure Parents can only view their own students
    if current_user.role == "PARENT":
        if not current_user.parent_profile or student.parent_id != current_user.parent_profile.id:
            raise HTTPException(status_code=403, detail="Not authorized to view this student")
            
    return student
