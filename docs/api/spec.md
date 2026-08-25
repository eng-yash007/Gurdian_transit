# REST & WebSocket API Specification

## 1. Global API Standards

- **Base URI Prefix**: `/api/v1`
- **Payload Format**: JSON (`application/json`)
- **Authentication**: Bearer JWT (`Authorization: Bearer <token>`)
- **Standard Success Format**:
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully"
}
```
- **Standard Error Format**:
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Student with ID 123 was not found",
    "details": []
  }
}
```

---

## 2. Core V1 Endpoint Modules

### 2.1 System & Health (`/api/v1/health`)
- `GET /api/v1/health`
  - Returns backend operational status, PostgreSQL database connection state, latency, and service version.

### 2.2 Authentication (`/api/v1/auth`)
- `POST /api/v1/auth/login` (Email, Password -> JWT Access Token + Role)
- `GET /api/v1/auth/me` (Current authenticated user profile)
- `POST /api/v1/auth/logout`

### 2.3 Management APIs (Admin Restricted)
- `/api/v1/students` (CRUD, assign parent, assign bus)
- `/api/v1/parents` (CRUD, list children)
- `/api/v1/buses` (CRUD, assign driver, status)
- `/api/v1/drivers` (CRUD, license info)
- `/api/v1/routes` (CRUD, waypoints, stops)
- `/api/v1/assignments` (Student-to-Bus/Route mappings)

### 2.4 Attendance Engine (`/api/v1/attendance`)
- `POST /api/v1/attendance/events` (Ingest BOARD / OFFBOARD event from AI or manual override)
- `GET /api/v1/attendance/daily` (Daily log by student or bus)
- `GET /api/v1/attendance/student/{id}` (Student historical attendance)

### 2.5 Computer Vision & Face Registration (`/api/v1/faces`)
- `POST /api/v1/faces/register/{student_id}` (Upload photo -> Quality check -> 512-dim embedding)
- `POST /api/v1/faces/verify` (Submit frame -> Detect -> Compare against active bus roster)

### 2.6 Telematics & GPS (`/api/v1/gps`)
- `POST /api/v1/gps/events` (Ingest GPS batch from edge IoT)
- `GET /api/v1/gps/buses/{bus_id}/live` (Latest coordinate & speed)

### 2.7 Alerts & Notifications
- `/api/v1/alerts` (List open alerts, acknowledge, resolve)
- `/api/v1/notifications` (List user notifications, mark as read)

### 2.8 WebSocket Channels (`/api/v1/ws`)
- `WS /api/v1/ws/live` (Real-time telemetry, attendance, and emergency broadcasts)
