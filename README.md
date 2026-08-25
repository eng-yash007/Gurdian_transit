# Guardian Transit AI 🛡️🚌

> **AI-Powered Smart School Bus Safety, Attendance, Tracking and Parent Monitoring Platform**

Guardian Transit AI is a state-of-the-art school transportation safety platform designed to elevate the safety, visibility, and accountability of students travelling in school buses.

---

## 🌟 Key Capabilities (System Vision)

- 🔍 **AI-Assisted Attendance**: Student face identification and automated boarding/offboarding logging.
- 📍 **Real-Time GPS Tracking**: High-frequency bus location updates on interactive maps for parents and administrators.
- 🔔 **Instant Parent Notifications**: Immediate updates when a child boards, exits, or when bus location milestones are reached.
- 🚨 **Proactive Safety & Alerts**: Unknown-person detection, route deviation alerts, and emergency incident logging.
- 👥 **Role-Based Portals**: Dedicated, secure dashboards for **Admins**, **Parents**, and **Drivers**.

---

## 🏗️ Architecture & Philosophy

The project follows a **Modular Monolith** pattern to ensure rapid iteration, clean domain separation, and maintainability without premature microservice complexity.

```
                    USERS (Admins & Parents)
                                |
             +------------------+------------------+
             |                                     |
             v                                     v
      Admin Dashboard                       Parent Dashboard
      (Next.js App)                         (Next.js App)
             |                                     |
             +------------------+------------------+
                                |
                                v
                       Backend API (FastAPI)
                                |
        +-----------------------+-----------------------+
        |                       |                       |
        v                       v                       v
    Database                AI/CV Core              Real-Time Engine
 (PostgreSQL/pgvector)   (Detection/Embeddings)   (WebSockets/Events)
```

---

## 📂 Repository Structure

```
guardian-transit-ai/
├── frontend/
│   └── next-app/           # Next.js 14+ (App Router), React, TypeScript, Tailwind CSS
├── backend/
│   ├── app/
│   │   ├── api/            # Versioned API routes (/api/v1/...)
│   │   ├── core/           # Config, database engine, security
│   │   ├── models/         # SQLAlchemy ORM entities
│   │   ├── schemas/        # Pydantic models for validation
│   │   ├── services/       # Core business logic
│   │   ├── repositories/   # Data access layer
│   │   └── main.py         # Application entry point
│   ├── alembic/            # Database migrations
│   ├── tests/              # Pytest automated test suites
│   ├── Dockerfile
│   └── requirements.txt
├── ai/                     # Computer Vision & Face Recognition pipelines (Phases 7-8)
├── edge-device/            # IoT Camera, GPS & Hardware daemons (Phase 14)
├── database/               # Database initialization & seed scripts
├── docs/                   # Architecture, ERD, API specs, and roadmap
├── docker/                 # Deployment configurations
├── scripts/                # Development & maintenance helper scripts
├── docker-compose.yml      # Local multi-container development environment
├── .env.example            # Environment variables template
└── README.md
```

---

## 🚀 Quick Start (Local Development)

### Option 1: Using Docker Compose (Recommended)

Make sure you have [Docker](https://www.docker.com/) and Docker Compose installed.

```bash
# 1. Copy environment variables
cp .env.example .env

# 2. Build and launch all services (Frontend, Backend, PostgreSQL)
docker compose up --build
```

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check Endpoint**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

### Option 2: Running Locally Without Docker

#### Prerequisites:
- Python 3.10+
- Node.js 18+ & npm
- PostgreSQL 15+ running locally (or via Docker: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=guardian_transit_db postgres:16-alpine`)

#### 1. Backend Setup:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run backend dev server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Frontend Setup:
```bash
cd frontend/next-app
npm install
npm run dev
```

---

## 🗺️ Development Roadmap

- [x] **Phase 0**: Architecture Documentation, Database ERD & Master Spec
- [x] **Phase 1**: Monorepo Foundation, FastAPI + Next.js + PostgreSQL Docker Environment
- [ ] **Phase 2**: Database Schema (ORM Models, Alembic Migrations, Seeds)
- [ ] **Phase 3**: Authentication (JWT, Passwords, Role-Based Access Control)
- [ ] **Phase 4**: Admin Dashboard (CRUD for Students, Parents, Buses, Drivers, Routes)
- [ ] **Phase 5**: Parent Dashboard (Child Profile, Status, Bus Overview)
- [ ] **Phase 6**: Attendance Engine (Simulated/Manual Boarding & Offboarding)
- [ ] **Phase 7**: Computer Vision (Face Detection & Quality Checking)
- [ ] **Phase 8**: Face Recognition (Feature Embeddings & Vector Matching)
- [ ] **Phase 9**: AI Attendance Pipeline Integration
- [ ] **Phase 10**: GPS Tracking & Route Mapping
- [ ] **Phase 11**: Real-Time WebSockets Engine
- [ ] **Phase 12**: Automated In-App & Multi-channel Notifications
- [ ] **Phase 13**: Proactive Safety, Deviation & Incident Alerts
- [ ] **Phase 14**: Edge Device & Hardware Simulator Integration
- [ ] **Phase 15**: Comprehensive Security Auditing & E2E Testing
- [ ] **Phase 16**: Cloud Deployment & CI/CD

---

## 🔒 Security & Privacy by Design

- Passwords hashed using industry-standard hashing algorithms (bcrypt/Argon2).
- Zero exposure of student face biometrics to unauthorized endpoints.
- Strict data isolation: Parents can exclusively query their own children's logs.
- Audit logs enabled for all administrative mutations.
