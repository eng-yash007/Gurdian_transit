# Guardian Transit AI 🛡️🚌

> **AI-Powered Smart School Bus Safety, Automated Facial Recognition Attendance, Telematics & Parent Monitoring Platform**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg?style=flat&logo=next.js&logoColor=white)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16%20%2B%20pgvector-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![DeepFace ArcFace](https://img.shields.io/badge/AI%20Vision-ArcFace%20512--d-FF6F00.svg?style=flat&logo=tensorflow&logoColor=white)](https://github.com/serengil/deepface)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

---

## 📖 Table of Contents
1. [Overview & Problem Statement](#-overview--problem-statement)
2. [Key Capabilities & Features](#-key-capabilities--features)
3. [System Architecture](#-system-architecture)
4. [Technology Stack](#-technology-stack)
5. [Repository Structure](#-repository-structure)
6. [Quick Start & How to Run](#-quick-start--how-to-run)
   - [Method 1: Docker Compose (Recommended)](#method-1-running-with-docker-compose-recommended)
   - [Method 2: Running Locally Without Docker](#method-2-running-locally-without-docker)
7. [Database Migrations & Seeding](#-database-migrations--seeding)
8. [Environment Variables Configuration](#-environment-variables-configuration)
9. [API Endpoints Reference](#-api-endpoints-reference)
10. [Current Progress vs Upcoming Roadmap](#-current-progress-vs-upcoming-roadmap)
11. [Security, Privacy & Data Isolation](#-security-privacy--data-isolation)

---

## 🌟 Overview & Problem Statement

School student transportation safety is one of the most vital responsibilities for educational institutions and parents. Traditional manual roll-calls and unmonitored bus rides suffer from:
- ❌ **Human Error & Delay**: Drivers manually checking lists cause boarding delays and missed attendance.
- ❌ **Lack of Parent Visibility**: Parents often have no real-time confirmation of when their child boarded, exited, or if they boarded the wrong bus.
- ❌ **Security Vulnerabilities**: Inability to immediately detect unauthorized individuals or strangers entering the school bus.

**Guardian Transit AI** is an intelligent, privacy-first platform that automates attendance logging using **AI Computer Vision (DeepFace ArcFace 512-d embeddings)**, performs instantaneous biometric vector search via **PostgreSQL `pgvector`**, tracks bus telemetry, and dispatches real-time safety alerts and parent notifications.

---

## 🚀 Key Capabilities & Features

- 👁️ **AI-Powered Facial Recognition**:
  - High-precision 512-dimensional facial embedding generation using ArcFace.
  - Sub-second vector similarity matching via PostgreSQL `pgvector` (`<=>` Cosine Distance).
  - Instant detection of authorized students vs. unregistered strangers.
- 📋 **Automated Attendance Engine**:
  - Dynamic event logging for `BOARD` and `OFFBOARD` actions.
  - Automatic student transit state management (`ON_BOARD` / `OFF_BOARD`).
  - Verification of student-to-bus assignments (flags students boarding an unassigned bus).
- 🚨 **Proactive Safety & Alerts Engine**:
  - Automatically logs `CRITICAL` alerts when an unknown/unauthorized person is detected.
  - Admin alert dashboard for rapid incident response.
- 📲 **Real-Time Parent Notifications**:
  - Automatic notification dispatch directly to parents when their child boards or offboards.
  - Strict data isolation: Parents can only access records for their own children.
- 🔐 **Role-Based Access Control (RBAC)**:
  - Secure JWT authentication with `passlib[bcrypt]` password hashing.
  - Distinct access tiers for `ADMIN`, `PARENT`, and `DRIVER`.
- 📊 **Interactive Diagnostics Portal**:
  - Next.js 14 dashboard verifying live database latency, API handshake, and system subsystem readiness.

---

## 🏗️ System Architecture

Guardian Transit AI is built on a high-velocity **Modular Monolith** architecture:

```
+--------------------------------------------------------------------------+
|                                CLIENTS                                   |
|   - Next.js Admin Portal (Fleet, Students, Alerts, AI Registration)      |
|   - Next.js Parent Portal (Child Status, History, Notifications)         |
+--------------------------------------------------------------------------+
                                     │
                                     │ HTTPS REST / WebSockets
                                     ▼
+--------------------------------------------------------------------------+
|                     APPLICATION LAYER (FastAPI Async)                    |
|                                                                          |
|   [ Versioned Endpoints: /api/v1/... ]                                   |
|   ├── auth          ├── students      ├── buses       ├── attendance     |
|   ├── ai (Vision)   ├── telemetry     ├── health                         |
|                                                                          |
|   [ Core Engines & Services ]                                            |
|   ├── VisionEngine (DeepFace ArcFace 512-d embeddings)                   |
|   ├── AttendanceEngine (State transitions, bus assignment validation)    |
|   ├── Security & JWT Token Manager (OAuth2 / RBAC)                       |
|   └── Database Engine (SQLAlchemy 2.0 Async Session Pool)                |
+--------------------------------------------------------------------------+
              │                                      │
              ▼                                      ▼
+------------------------------------+  +----------------------------------+
|          DATABASE ENGINE           |  |           AI / CV CORE           |
|  PostgreSQL 16 + pgvector          |  |  DeepFace & ArcFace              |
|  (Relational ORM + Vector Search)  |  |  (OpenCV Image Pipeline)         |
+------------------------------------+  +----------------------------------+
```

---

## 💻 Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | **Next.js 14 (App Router)** | Modern React framework with Server & Client components |
| **Styling & UI** | **Tailwind CSS + Lucide Icons** | Responsive dark-mode dashboard and rich typography |
| **Backend API** | **FastAPI (Python 3.10+)** | High-performance asynchronous REST API |
| **ORM & DB Layer** | **SQLAlchemy 2.0 + AsyncPG** | Asynchronous database queries and relationship mapping |
| **Database Migrations** | **Alembic** | Automated database schema versioning |
| **Database** | **PostgreSQL 16 + pgvector** | ACID relational storage + vector similarity index |
| **Computer Vision** | **DeepFace (ArcFace) + OpenCV** | 512-d face embedding generation and face detection |
| **Security** | **Jose JWT + Passlib (Bcrypt)** | Stateless token authentication and password hashing |
| **Orchestration** | **Docker & Docker Compose** | Multi-container local and production deployment |

---

## 📂 Repository Structure

```
guardian-transit-ai/
├── backend/
│   ├── alembic/                    # Database migration scripts
│   │   ├── versions/               # Versioned migration files
│   │   └── env.py                  # Alembic runtime configuration
│   ├── app/
│   │   ├── ai/
│   │   │   └── vision.py           # DeepFace ArcFace embedding extractor
│   │   ├── api/
│   │   │   ├── deps.py             # Auth & DB dependency injectors
│   │   │   └── v1/
│   │   │       ├── api.py          # Unified API router
│   │   │       └── endpoints/      # REST route handlers
│   │   │           ├── ai.py       # Face registration & recognition
│   │   │           ├── attendance.py # Attendance logs & manual override
│   │   │           ├── auth.py     # Login, JWT tokens & user profiles
│   │   │           ├── buses.py    # Fleet & bus management
│   │   │           ├── health.py   # Diagnostics & DB ping
│   │   │           ├── students.py # Student profile & parent queries
│   │   │           └── telemetry.py# Alerts and notifications
│   │   ├── core/
│   │   │   ├── config.py           # Application settings & environment vars
│   │   │   ├── database.py         # Async SQLAlchemy engine & health check
│   │   │   └── security.py         # Password hashing & JWT helper functions
│   │   ├── models/                 # SQLAlchemy ORM database models
│   │   │   ├── attendance.py       # Attendance record model
│   │   │   ├── face_profile.py     # 512-d Vector embedding model (pgvector)
│   │   │   ├── fleet.py            # Bus, Route, BusStop, BusAssignment
│   │   │   ├── student.py          # Student model
│   │   │   ├── telemetry.py        # Alert & Notification models
│   │   │   └── user.py             # User, Parent, Driver models
│   │   ├── schemas/                # Pydantic validation schemas
│   │   ├── services/
│   │   │   └── attendance_engine.py# Attendance business logic & alert dispatch
│   │   └── main.py                 # FastAPI application entry point
│   ├── scripts/
│   │   └── seed_db.py              # Mock data database seeder (Faker)
│   ├── tests/                      # Automated test suite (Pytest)
│   ├── Dockerfile                  # Production container recipe with CV libs
│   └── requirements.txt            # Python dependencies
├── frontend/
│   └── next-app/
│       ├── src/
│       │   └── app/                # Next.js App Router pages and styles
│       ├── public/                 # Static web assets
│       ├── Dockerfile              # Next.js standalone container
│       ├── package.json            # Node.js dependencies & scripts
│       ├── tailwind.config.ts      # Tailwind CSS theme configuration
│       └── tsconfig.json           # TypeScript configuration
├── docs/                           # Architectural specs, ERD & roadmap
├── docker-compose.yml              # Local multi-service environment
├── .env.example                    # Environment variables template
├── .gitignore                      # Git exclusion rules
└── README.md                       # Master project documentation
```

---

## 🚀 Quick Start & How to Run

### Method 1: Running with Docker Compose (Recommended)

This is the fastest method to start all services (PostgreSQL with `pgvector`, FastAPI Backend, and Next.js Frontend) in isolated containers.

#### 1. Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (macOS / Linux / Windows).

#### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/eng-yash007/Gurdian_transit.git
cd Gurdian_transit

# Copy environment variables template
cp .env.example .env
```

#### 3. Build and Start All Containers
```bash
docker compose up --build
```

#### 4. Access the Application
- 🌐 **Frontend Diagnostics Portal**: [http://localhost:3000](http://localhost:3000)
- ⚙️ **Backend REST API**: [http://localhost:8000](http://localhost:8000)
- 📚 **Interactive Swagger API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 🩺 **Health Check API**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

### Method 2: Running Locally Without Docker

If you prefer running the services directly on your host machine:

#### Prerequisites
- **Python**: 3.10, 3.11, or 3.12
- **Node.js**: 18+ and `npm`
- **PostgreSQL 16** with the `pgvector` extension installed.
  *(Quick Docker command for DB only)*:
  ```bash
  docker run -d --name pgvector-db -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=guardian_transit_db pgvector/pgvector:pg16
  ```

#### 1. Environment Setup
```bash
cp .env.example .env
```

#### 2. Backend Setup
```bash
cd backend

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# (Optional) Seed the database with mock test data
python scripts/seed_db.py

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Frontend Setup
```bash
cd frontend/next-app

# Install dependencies
npm install

# Start Next.js development server
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🗄️ Database Migrations & Seeding

### Running Alembic Migrations
```bash
cd backend
# Apply all latest migrations
alembic upgrade head

# Generate a new migration when modifying SQLAlchemy models
alembic revision --autogenerate -m "describe_your_changes"
```

### Seeding Mock Data
We have provided a comprehensive seed script (`backend/scripts/seed_db.py`) that generates realistic mock data using `Faker`:
- 1 Admin user (`admin@school.com` / `password123`)
- 1 Driver user & driver profile (`driver1@school.com` / `password123`)
- 1 Parent user & profile (`parent1@school.com` / `password123`)
- 1 Student assigned to Parent
- 1 Bus (`BUS-101`) & Route (`Morning Route A`)
- 1 BusAssignment linking Student + Bus + Route
- 1 FaceProfile with a 512-dimensional vector embedding

Run the seeder:
```bash
cd backend
python scripts/seed_db.py
```

---

## ⚙️ Environment Variables Configuration

The `.env.example` file contains all necessary configuration variables:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `PROJECT_NAME` | `Guardian Transit AI` | Display name of the application |
| `ENVIRONMENT` | `development` | Runtime environment (`development` / `production`) |
| `DEBUG` | `true` | Enable debug logs |
| `POSTGRES_USER` | `postgres` | PostgreSQL username |
| `POSTGRES_PASSWORD` | `postgres` | PostgreSQL password |
| `POSTGRES_SERVER` | `localhost` | PostgreSQL host |
| `POSTGRES_PORT` | `5432` | PostgreSQL port |
| `POSTGRES_DB` | `guardian_transit_db` | Database name |
| `DATABASE_URL` | `postgresql+asyncpg://...` | Async connection string for FastAPI |
| `SYNC_DATABASE_URL` | `postgresql://...` | Sync connection string for Alembic |
| `SECRET_KEY` | *(Secret String)* | Secret key for signing JWT tokens |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | JWT token validity (in minutes) |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend API URL used by frontend |
| `PORT` | `3000` | Port for the Next.js frontend |
| `CORS_ORIGINS` | `["http://localhost:3000", ...]` | Allowed CORS origins for browser security |

---

## 📡 API Endpoints Reference

Explore the full interactive documentation at `http://localhost:8000/docs`.

### 1. Authentication (`/api/v1/auth`)
| Method | Path | Summary | Access |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/login` | JSON login for web clients (Returns JWT) | Public |
| `POST` | `/api/v1/auth/login/access-token` | OAuth2 form login for Swagger docs | Public |
| `GET` | `/api/v1/auth/me` | Fetch logged-in user details & role | Authenticated |

### 2. AI Facial Recognition (`/api/v1/ai`)
| Method | Path | Summary | Access |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/ai/register` | Upload photo & generate 512-d face embedding | `ADMIN` |
| `POST` | `/api/v1/ai/recognize` | Live photo matching via `pgvector` Cosine distance. Triggers attendance or alert | Authenticated / Edge |

### 3. Students & Parents (`/api/v1/students`)
| Method | Path | Summary | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/students/me` | Get all children linked to current Parent | `PARENT` |
| `GET` | `/api/v1/students/{student_id}` | Get specific student profile | `ADMIN` / Authorized `PARENT` |

### 4. Fleet & Buses (`/api/v1/buses`)
| Method | Path | Summary | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/buses/` | List all school buses, license plates & capacities | Authenticated |

### 5. Attendance (`/api/v1/attendance`)
| Method | Path | Summary | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/attendance/student/{student_id}` | Get attendance timeline for a student | `ADMIN` / Authorized `PARENT` |
| `POST` | `/api/v1/attendance/manual` | Record manual attendance override | Authenticated |

### 6. Telemetry & Alerts (`/api/v1/telemetry`)
| Method | Path | Summary | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/telemetry/alerts` | List critical system alerts (unauthorized faces, etc.) | `ADMIN` |
| `GET` | `/api/v1/telemetry/notifications` | List boarding notifications | `ADMIN` / `PARENT` |

### 7. Health Check (`/api/v1/health`)
| Method | Path | Summary | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Live database connectivity ping & subsystem status | Public |

---

## 📊 Current Progress vs Upcoming Roadmap

```
Progress: [====================================>-----------------] 50% Complete
```

### ✅ Completed Milestones (Phases 0 - 6)
- [x] **Phase 0**: Architecture blueprint, ERD schema design, and master specification.
- [x] **Phase 1**: Monorepo structure, Docker Compose setup, Next.js frontend and FastAPI backend health integration.
- [x] **Phase 2**: Full relational & vector database schema, Alembic migration scripts, and Faker mock database seeder.
- [x] **Phase 3**: JWT authentication with bcrypt password encryption, OAuth2 compatibility, and Role-Based Access Control (`ADMIN`, `PARENT`, `DRIVER`).
- [x] **Phase 4**: Core REST domain endpoints (Students, Parents, Buses, Routes, Attendance records).
- [x] **Phase 5**: DeepFace ArcFace 512-d AI Vision pipeline, face registration, and live recognition with pgvector Cosine similarity search.
- [x] **Phase 6**: Attendance Engine state machine (`BOARD` / `OFFBOARD`), automatic parent notification dispatcher, and unknown stranger security alert engine.

### ⏳ Upcoming Milestones (Phases 7 - 12)
- [ ] **Phase 7: Real-Time WebSockets Engine**: Broadcast bus coordinates and instant live attendance events to open web clients.
- [ ] **Phase 8: Full Next.js Web Portals**:
  - **Admin Dashboard**: Student management, face enrollment UI, interactive route mapping, and real-time security alert feeds.
  - **Parent Dashboard**: Real-time bus tracking map, child boarding status cards, and notification timeline.
- [ ] **Phase 9: IoT Hardware & Edge Simulator**: Python simulator for on-bus Raspberry Pi / Jetson cameras and GPS NMEA stream.
- [ ] **Phase 10: Multi-Channel Alerts**: WhatsApp, SMS, and Web Push notifications via Twilio & Firebase Cloud Messaging (FCM).
- [ ] **Phase 11: Route Geofencing & ETA Engine**: Automated alerts when bus is 5 minutes from a stop; route deviation alarms.
- [ ] **Phase 12: Production Cloud CI/CD Deployment**: Automated GitHub Actions testing, Docker image packaging, and cloud deployment.

---

## 🔒 Security, Privacy & Data Isolation

- 🛡️ **Zero Raw Biometric Exposure**: Raw facial images are processed in-memory and discarded after extracting the 512-dimensional vector embedding.
- 🔐 **Parent Scoped Data Isolation**: Endpoints strictly enforce multi-tenant isolation; parents can never query data or attendance records belonging to other students.
- 🔑 **Cryptographic Hashing**: All passwords are encrypted with `bcrypt` (work factor 12) before persistence.
- 🚫 **Strict Git Hygiene**: Secrets, credentials, `.env` files, virtual environments, build artifacts, and test media are strictly excluded from version control.

---

## 🤝 Contributing & License

1. Fork the Project & Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
2. Commit your Changes (`git commit -m 'feat: add some AmazingFeature'`)
3. Push to the Branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

*Guardian Transit AI &copy; 2026. All rights reserved.*
