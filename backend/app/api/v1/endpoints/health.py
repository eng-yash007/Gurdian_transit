from datetime import datetime, timezone
from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.database import check_database_health

router = APIRouter()


class DatabaseHealth(BaseModel):
    status: str
    latency_ms: float
    database_name: Optional[str] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    project: str
    version: str
    environment: str
    timestamp: str
    database: DatabaseHealth
    subsystems: Dict[str, str]


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="System and Database Health Check",
    description="Returns backend API health status, live database connectivity, and subsystem statuses.",
)
async def get_system_health() -> HealthResponse:
    db_health = await check_database_health()
    is_healthy = db_health.get("status") == "connected"

    return HealthResponse(
        status="healthy" if is_healthy else "degraded",
        project=settings.PROJECT_NAME,
        version="0.1.0",
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc).isoformat(),
        database=DatabaseHealth(
            status=db_health.get("status", "unknown"),
            latency_ms=db_health.get("latency_ms", 0.0),
            database_name=db_health.get("database_name"),
            error=db_health.get("error"),
        ),
        subsystems={
            "api_server": "online",
            "attendance_engine": "standby (phase 6)",
            "face_recognition_cv": "standby (phase 7-8)",
            "gps_telematics": "standby (phase 10)",
            "realtime_websockets": "standby (phase 11)",
        },
    )
