# System Architecture Overview - Guardian Transit AI

## 1. Executive Summary

Guardian Transit AI is an intelligent school transportation safety and tracking platform. It unifies Computer Vision (Face Recognition), IoT Edge Telematics (GPS and bus event stream), and real-time parent-admin monitoring into a dependable, privacy-focused solution.

---

## 2. Architectural Blueprint: Modular Monolith

To prioritize development velocity, clean maintainability, and straightforward debugging, the system starts as a **Modular Monolith**:

```
+-----------------------------------------------------------------------+
|                           CLIENT LAYER                                |
|  - Next.js Admin Portal (Fleet, Student, Route, AI & Alert Management)|
|  - Next.js Parent Portal (Live Tracking, Status, Notifications)       |
|  - Driver Telematics UI (Optional / Future)                           |
+-----------------------------------------------------------------------+
                                  |
                                  | HTTPS / WSS
                                  v
+-----------------------------------------------------------------------+
|                    APPLICATION LAYER (FastAPI)                        |
|                                                                       |
|  [ API Layer: /api/v1/... ]                                           |
|    ├── auth        ├── students      ├── buses       ├── attendance   |
|    ├── parents     ├── drivers       ├── routes      ├── gps          |
|    ├── faces       ├── alerts        ├── notifications                |
|                                                                       |
|  [ Domain Services ]                                                  |
|    ├── AuthService                   ├── StudentService               |
|    ├── AttendanceEngine              ├── GPSTrackingService           |
|    ├── NotificationDispatcher        ├── SafetyAlertEngine            |
|                                                                       |
|  [ Data Access & Repositories ]                                       |
|    └── SQLAlchemy ORM with Connection Pooling & Transaction Mgmt      |
+-----------------------------------------------------------------------+
         |                       |                         |
         v                       v                         v
+------------------+    +-------------------+    +--------------------+
|  STORAGE LAYER   |    |    AI/CV CORE     |    | REAL-TIME BUS      |
|  PostgreSQL 16   |    |  InsightFace/Arc  |    | WebSocket Manager  |
|  (with pgvector) |    |  Vector Matcher   |    | (Broadcast Stream) |
+------------------+    +-------------------+    +--------------------+
```

---

## 3. Core Subsystems

### 3.1 Authentication & Authorization
- **JWT (JSON Web Tokens)**: Stateless access tokens containing user claims (`sub`, `role`, `exp`).
- **RBAC**: Strict role-based permissions (`ADMIN`, `PARENT`, `DRIVER`).
- **Data Isolation**: Multi-tenant scoped queries ensuring parents can only access records associated with their registered children.

### 3.2 Attendance Engine
- Manages discrete student transit state: `OFF_BOARD` <-> `ON_BOARD`.
- Resolves face recognition match scores or manual fallback scans against active bus assignments and routes.
- Dispatches event records (`BOARD`, `OFFBOARD`, `ABSENT`).

### 3.3 Computer Vision Pipeline
- **Face Detection**: Fast multi-angle detection generating clean bounding boxes.
- **Quality & Alignment**: Evaluates pose angles, illumination, and blur before vector extraction.
- **Embedding Generation**: Produces 512-dimensional normalized float vectors.
- **Vector Matching**: Cosine similarity against stored `FaceProfile` embeddings with calibrated confidence thresholds.

### 3.4 Telematics & GPS Tracking
- Ingests latitude, longitude, speed, timestamp, and heading from edge bus hardware.
- Updates in-memory bus location cache and persists historical GPS tracks.
- Pushes live updates to connected WebSocket subscribers.

### 3.5 Real-Time Communication
- Native FastAPI WebSocket endpoints broadcasting structured payloads for:
  - `BUS_LOCATION_UPDATED`
  - `STUDENT_BOARDED` / `STUDENT_OFFBOARDED`
  - `SAFETY_ALERT_TRIGGERED`
  - `EMERGENCY_BROADCAST`

---

## 4. Hardware Integration Strategy

```
+-------------------------------------------------------------+
|                 BUS EDGE HARDWARE (IoT Box)                 |
|                                                             |
|  +----------------+    +----------------+    +-----------+  |
|  |  CCTV Camera   |    |  GPS Receiver  |    | Panic Btn |  |
|  +----------------+    +----------------+    +-----------+  |
|         │                     │                    │        |
|         ▼                     ▼                    ▼        |
|  [ Edge Agent / Camera & Telematics Ingestion Daemon ]      |
+-------------------------------------------------------------+
                                │
               mTLS / Token-Authenticated REST / WSS
                                │
                                ▼
                   Backend Telematics Ingestion
```
