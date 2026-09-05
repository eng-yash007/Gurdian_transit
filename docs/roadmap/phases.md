# Development Roadmap & Phase Milestones

This roadmap tracks the development phases and progress of the **Guardian Transit AI** platform.

---

### Phase 0: Planning, Architecture & Specification (Completed ✅)
- [x] Comprehensive Architecture Blueprint (Modular Monolith)
- [x] Relational Database Schema & pgvector ERD Design
- [x] REST & WebSocket API Specification
- [x] Master Roadmap & Milestone Definition

### Phase 1: Monorepo Foundation & Infrastructure (Completed ✅)
- [x] Monorepo directory structure setup
- [x] Docker Compose multi-container environment (Next.js 14, FastAPI, PostgreSQL 16 + pgvector)
- [x] Backend FastAPI skeleton with `/api/v1/health` and live database connectivity check
- [x] Frontend Next.js landing & live infrastructure diagnostics matrix dashboard
- [x] Comprehensive README, `.gitignore`, and `.env.example` configuration

### Phase 2: Database Schema, ORM Models & Migrations (Completed ✅)
- [x] SQLAlchemy 2.0 Async ORM entity models (`User`, `Parent`, `Driver`, `Student`, `Bus`, `Route`, `BusStop`, `BusAssignment`, `Attendance`, `FaceProfile`, `Alert`, `Notification`)
- [x] PostgreSQL `pgvector` extension integration for 512-dimensional face embeddings
- [x] Alembic migration initialization (`d379b419b233_initial_schema.py`)
- [x] Database seeding script (`backend/scripts/seed_db.py`) with Faker mock data (Admin, Parents, Students, Buses, Routes, Face Profiles)

### Phase 3: Authentication, JWT & Role-Based Access Control (Completed ✅)
- [x] Password hashing using `passlib[bcrypt]`
- [x] JWT token issuance, verification, and expiration handling (`python-jose`)
- [x] OAuth2 login endpoint (`/api/v1/auth/login/access-token`) and JSON login (`/api/v1/auth/login`)
- [x] Current user profile endpoint (`/api/v1/auth/me`)
- [x] Role-Based Access Control dependencies (`ADMIN`, `PARENT`, `DRIVER`)
- [x] Automated pytest authentication test suites

### Phase 4: Core Domain REST APIs (Completed ✅)
- [x] Student endpoints (`/api/v1/students/me`, `/api/v1/students/{student_id}`) with parent data isolation
- [x] Bus & fleet endpoints (`/api/v1/buses/`)
- [x] Attendance retrieval endpoints (`/api/v1/attendance/student/{student_id}`)
- [x] Manual attendance override endpoint (`/api/v1/attendance/manual`)

### Phase 5: AI Computer Vision & Vector Recognition Pipeline (Completed ✅)
- [x] `VisionEngine` face embedding extractor using DeepFace (ArcFace model, 512-dim normalized vectors)
- [x] Face registration endpoint (`/api/v1/ai/register`) storing biometric vectors in `pgvector`
- [x] Live face recognition endpoint (`/api/v1/ai/recognize`) with Cosine similarity vector distance search (`<=>` operator)
- [x] OpenCV / DeepFace headless dependencies configured in backend `Dockerfile`

### Phase 6: Attendance Engine & Telemetry Alerts (Completed ✅)
- [x] `AttendanceEngine` event processor (`BOARD`, `OFFBOARD`, `WRONG_BUS`)
- [x] Automatic parent notification generation on boarding / offboarding events
- [x] Automatic security alert creation on unauthorized stranger face detections
- [x] Telemetry endpoints for viewing alerts (`/api/v1/telemetry/alerts`) and parent notifications (`/api/v1/telemetry/notifications`)

---

## 🔮 Upcoming Phases (Future Roadmap)

### Phase 7: Real-Time WebSockets Engine (Next Up ⏳)
- [ ] WebSocket connection manager in FastAPI (`/ws/telemetry`, `/ws/attendance`)
- [ ] Real-time bus GPS telemetry broadcast to connected dashboards
- [ ] Live attendance event push notifications to parent browser clients

### Phase 8: Full-Featured Frontend Web Portals (In Progress ⏳)
- [ ] **Admin Portal UI**:
  - [ ] Fleet management (Buses, Drivers, Routes, Bus Stops)
  - [ ] Student & Parent directory with face profile registration modal
  - [ ] Live security alert feed with audio/visual warnings
- [ ] **Parent Portal UI**:
  - [ ] Child transit status overview (On Bus / At School / At Home)
  - [ ] Live interactive bus tracking map (Leaflet / Mapbox)
  - [ ] Notification history timeline

### Phase 9: IoT Edge Hardware Simulator (⏳)
- [ ] Python-based bus hardware simulator (Simulated camera frame feed & GPS NMEA coordinate stream)
- [ ] Edge device automated event submission daemon

### Phase 10: Multi-Channel Notifications (⏳)
- [ ] WhatsApp & SMS notification dispatch via Twilio / Fast2SMS
- [ ] Web Push / Firebase Cloud Messaging (FCM) integration

### Phase 11: Route Geofencing & ETA Predictions (⏳)
- [ ] Bus stop geofence trigger (notifying parents 5 minutes before arrival)
- [ ] Route deviation alerts when bus deviates from assigned route

### Phase 12: Production Hardening, CI/CD & Cloud Deployment (⏳)
- [ ] End-to-end integration test suite
- [ ] GitHub Actions CI/CD workflows for automated testing and Docker container builds
- [ ] Cloud deployment manifest (AWS ECS / GCP Cloud Run / Kubernetes)
