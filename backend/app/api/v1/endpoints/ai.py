from typing import Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import UUID4

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.student import Student
from app.models.fleet import Bus
from app.models.face_profile import FaceProfile
from app.models.telemetry import Alert
from app.ai.vision import VisionEngine
from app.services.attendance_engine import AttendanceEngine

router = APIRouter()

# ArcFace usually requires Cosine Distance for robust matching.
# Cosine distance < 0.40 is generally a solid match for ArcFace.
MATCH_THRESHOLD = 0.40 

@router.post("/register")
async def register_face(
    student_id: UUID4 = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Extracts a 512-d facial embedding from the uploaded image and 
    saves it to the student's profile in the database.
    """
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Only Admins can register faces.")
        
    # Check student exists
    result = await db.execute(select(Student).where(Student.id == student_id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Student not found")
        
    image_bytes = await file.read()
    
    try:
        embedding = VisionEngine.extract_embedding(image_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    # Save to pgvector table
    face_profile = FaceProfile(
        student_id=student_id,
        model_version=VisionEngine.MODEL_NAME,
        embedding=embedding,
        quality_score=0.9 # Hardcoded for MVP, could be dynamic
    )
    db.add(face_profile)
    await db.commit()
    
    return {"message": "Face registered successfully", "student_id": str(student_id)}


@router.post("/recognize")
async def recognize_face(
    bus_id: UUID4 = Form(...),
    event_type: str = Form("BOARD"), # BOARD or OFFBOARD
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Takes a live picture, extracts the embedding, compares it against the database.
    If match found: Records attendance.
    If unknown: Generates a CRITICAL alert.
    """
    # Check bus exists
    result = await db.execute(select(Bus).where(Bus.id == bus_id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Bus not found")
        
    image_bytes = await file.read()
    
    try:
        live_embedding = VisionEngine.extract_embedding(image_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    # pgvector Cosine distance search (<=> operator)
    # Order by distance, get the closest one
    result = await db.execute(
        select(FaceProfile, FaceProfile.embedding.cosine_distance(live_embedding).label("distance"))
        .order_by("distance")
        .limit(1)
    )
    
    match_record = result.first()
    
    if not match_record:
        # No faces in the database at all
        raise HTTPException(status_code=404, detail="No registered faces in database")
        
    closest_profile, distance = match_record
    
    if distance > MATCH_THRESHOLD:
        # UNKNOWN PERSON DETECTED
        alert = Alert(
            alert_type="UNAUTHORIZED_PERSON",
            severity="CRITICAL",
            bus_id=bus_id,
            description=f"Unknown face detected. Distance: {distance:.2f}"
        )
        db.add(alert)
        await db.commit()
        return {"status": "UNKNOWN", "message": "Unauthorized person detected. Alert generated.", "distance": distance}
        
    # MATCH FOUND! Trigger Attendance Engine
    confidence = max(0.0, 1.0 - (distance / MATCH_THRESHOLD)) # Simple confidence calc
    
    attendance = await AttendanceEngine.process_attendance_event(
        db=db,
        student_id=closest_profile.student_id,
        bus_id=bus_id,
        event_type=event_type,
        verification_method="AI_FACE",
        confidence_score=confidence
    )
    
    return {
        "status": "MATCH", 
        "student_id": str(closest_profile.student_id),
        "confidence": confidence,
        "event_recorded": event_type
    }
