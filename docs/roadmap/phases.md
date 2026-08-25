# Development Roadmap & Phase Milestones

This roadmap executes the **Guardian Transit AI Master Specification** sequentially.

---

### Phase 0: Planning & Documentation (Completed)
- [x] Comprehensive Architecture Blueprint
- [x] Database Schema & ERD
- [x] REST & WebSocket API Specification
- [x] Master Roadmap & Milestones

### Phase 1: Project Foundation & Infrastructure (Current)
- [x] Monorepo structure setup
- [x] Docker Compose multi-container environment (Next.js, FastAPI, PostgreSQL)
- [x] Backend FastAPI skeleton with `/api/v1/health` and live database connectivity check
- [x] Frontend Next.js landing & system diagnostics dashboard
- [x] Comprehensive README, .gitignore, and .env configuration

### Phase 2: Database Schema & Migrations
- [ ] SQLAlchemy ORM entity definitions
- [ ] Alembic migration initialization
- [ ] Database seeds for initial mock testing (Admin, Parents, Students, Buses, Routes)

### Phase 3: Authentication & Authorization
- [ ] User authentication with password hashing (bcrypt)
- [ ] JWT token issuance and refresh
- [ ] Role-based Access Control (`ADMIN`, `PARENT`, `DRIVER`)
- [ ] Protected endpoints and frontend auth guards

### Phase 4: Admin Dashboard
- [ ] School management portal UI
- [ ] Student, Parent, Bus, Driver, and Route management (CRUD)
- [ ] Bus and route assignment engine

### Phase 5: Parent Dashboard
- [ ] Parent-focused portal UI
- [ ] Child transit status cards (Boarding status, assigned bus, last seen)
- [ ] Parent view isolation security verification

### Phase 6: Core Attendance Engine (Manual/Simulated)
- [ ] Attendance event ingestion (`BOARD` / `OFFBOARD`)
- [ ] Status transition state machine
- [ ] Verification without computer vision dependencies

### Phase 7: Computer Vision Foundation
- [ ] OpenCV and pretrained face detector integration
- [ ] Face cropping, bounding box normalization, and quality validation

### Phase 8: Face Recognition & Vector Matching
- [ ] 512-dimensional facial embedding generation
- [ ] Vector similarity calculation with calibrated matching thresholds
- [ ] Face profile registration service

### Phase 9: AI + Attendance Integration
- [ ] End-to-end pipeline: Frame Ingestion -> Face Match -> Attendance Event -> State Update

### Phase 10: GPS & Telematics
- [ ] GPS coordinate ingestion pipeline
- [ ] Real-time bus location cache and historical path recording
- [ ] Map rendering with Leaflet

### Phase 11: Real-Time WebSockets Engine
- [ ] WebSocket hub for live telemetry and attendance broadcasts
- [ ] Dynamic frontend map updates and status badges

### Phase 12: Notification System
- [ ] In-app notification dispatcher
- [ ] Real-time push to parent dashboard

### Phase 13: Safety & Proactive Alerts
- [ ] Unknown-person detection handling
- [ ] Route deviation alerts
- [ ] Emergency alert logging & broadcasts

### Phase 14: Edge Hardware Simulator
- [ ] Python simulator for on-bus camera feeds and GPS beacons

### Phase 15: Security Auditing & E2E Verification
- [ ] Automated end-to-end testing suite
- [ ] Vulnerability scanning and performance benchmarks

### Phase 16: Deployment & Production Readiness
- [ ] Production build verification
- [ ] CI/CD pipeline automation
