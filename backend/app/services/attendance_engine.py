from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import UUID4

from app.models.attendance import Attendance
from app.models.student import Student
from app.models.fleet import BusAssignment
from app.models.telemetry import Notification, Alert

class AttendanceEngine:
    @staticmethod
    async def process_attendance_event(
        db: AsyncSession,
        student_id: UUID4,
        bus_id: UUID4,
        event_type: str, # BOARD | OFFBOARD
        verification_method: str = "AI_FACE",
        confidence_score: Optional[float] = None
    ) -> Attendance:
        """
        Core business logic for recording attendance, updating state, and triggering alerts.
        """
        # 1. Fetch Student
        result = await db.execute(select(Student).where(Student.id == student_id))
        student = result.scalars().first()
        if not student:
            raise ValueError("Student not found")

        # 2. Record Attendance Event
        attendance = Attendance(
            student_id=student_id,
            bus_id=bus_id,
            event_type=event_type,
            verification_method=verification_method,
            confidence_score=confidence_score
        )
        db.add(attendance)

        # 3. Update Student State
        student.current_status = event_type

        # 4. Create Parent Notification
        notification = Notification(
            user_id=student.parent.user_id if student.parent else None,
            title="Attendance Update",
            message=f"{student.first_name} {student.last_name} has {event_type.lower()}ed the bus.",
            notification_type="ATTENDANCE"
        )
        if notification.user_id:
            db.add(notification)

        # 5. Anomaly Detection: Did they board the right bus?
        if event_type == "BOARD":
            # Check if this student is assigned to this bus
            result = await db.execute(
                select(BusAssignment)
                .where(BusAssignment.student_id == student_id)
                .where(BusAssignment.bus_id == bus_id)
                .where(BusAssignment.is_active == True)
            )
            assignment = result.scalars().first()
            
            if not assignment:
                # WRONG BUS ALERT
                alert = Alert(
                    alert_type="WRONG_BUS",
                    severity="HIGH",
                    bus_id=bus_id,
                    student_id=student_id,
                    description=f"{student.first_name} {student.last_name} boarded unassigned bus."
                )
                db.add(alert)
        
        await db.commit()
        await db.refresh(attendance)
        
        return attendance
