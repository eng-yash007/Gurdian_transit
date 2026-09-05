from fastapi import APIRouter
from app.api.v1.endpoints import health, auth, students, buses, attendance, ai, telemetry

api_router = APIRouter()

# Register core health & diagnostic endpoints
api_router.include_router(health.router, tags=["System Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(students.router, prefix="/students", tags=["Students"])
api_router.include_router(buses.router, prefix="/buses", tags=["Buses"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI Vision"])
api_router.include_router(telemetry.router, prefix="/telemetry", tags=["Telemetry & Alerts"])

