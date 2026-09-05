from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.telemetry import Alert, Notification

router = APIRouter()

@router.get("/alerts", summary="Get System Alerts")
async def get_alerts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve all critical alerts (like unauthorized face detections).
    Only Admins should see this.
    """
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    result = await db.execute(
        select(Alert)
        .order_by(Alert.created_at.desc())
        .limit(50)
    )
    alerts = result.scalars().all()
    
    return [
        {
            "id": alert.id,
            "alert_type": alert.alert_type,
            "severity": alert.severity,
            "description": alert.description,
            "created_at": alert.created_at
        }
        for alert in alerts
    ]

@router.get("/notifications", summary="Get Parent Notifications")
async def get_notifications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve notifications (e.g. Attendance updates).
    If Admin, returns all. If Parent, returns only their own.
    """
    query = select(Notification).order_by(Notification.created_at.desc()).limit(50)
    
    if current_user.role == "PARENT":
        query = query.where(Notification.user_id == current_user.id)
        
    result = await db.execute(query)
    notifications = result.scalars().all()
    
    return [
        {
            "id": notif.id,
            "title": notif.title,
            "message": notif.message,
            "is_read": notif.is_read,
            "created_at": notif.created_at
        }
        for notif in notifications
    ]
