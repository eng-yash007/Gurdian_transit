# Database Design & Entity-Relationship Specification

## 1. Database Principles

- **Primary Keys**: UUID v4 / BigInt for high scalability and secure references.
- **Auditability**: All primary tables feature `created_at` and `updated_at` UTC timestamps.
- **Referential Integrity**: Foreign keys enforce cascade or restrict policies appropriately.
- **Vector Support**: `pgvector` extension for indexing 512-dim facial embeddings with HNSW indexing.
- **Soft Deletion**: `is_active` / `deleted_at` flags where historical tracking is essential.

---

## 2. Mermaid Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    User ||--o| Admin : "is a"
    User ||--o| Parent : "is a"
    User ||--o| Driver : "is a"
    User ||--o{ Notification : "receives"

    Parent ||--|{ Student : "guardian of"
    
    Bus ||--o| Driver : "driven by"
    Bus ||--o{ BusAssignment : "assigned to"
    Bus ||--o{ GPSEvent : "transmits"
    Bus ||--o{ Alert : "generates"
    Bus ||--o{ Attendance : "logs"

    Route ||--o{ BusAssignment : "assigned via"
    Route ||--o{ BusStop : "contains"

    Student ||--o{ BusAssignment : "assigned to"
    Student ||--o{ FaceProfile : "has biometric"
    Student ||--o{ Attendance : "records"
    Student ||--o{ Alert : "referenced in"

    User {
        uuid id PK
        string email UK
        string hashed_password
        string role "ADMIN | PARENT | DRIVER"
        string full_name
        string phone_number
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    Parent {
        uuid id PK
        uuid user_id FK
        string emergency_contact
        string address
    }

    Driver {
        uuid id PK
        uuid user_id FK
        string license_number UK
        string phone_number
        boolean is_available
    }

    Bus {
        uuid id PK
        string bus_number UK
        string license_plate UK
        int capacity
        uuid current_driver_id FK
        string status "ACTIVE | INACTIVE | MAINTENANCE"
        timestamp created_at
    }

    Route {
        uuid id PK
        string name
        string description
        jsonb waypoints
        string start_point
        string end_point
        boolean is_active
    }

    BusStop {
        uuid id PK
        uuid route_id FK
        string stop_name
        float latitude
        float longitude
        int sequence_order
        time scheduled_time
    }

    BusAssignment {
        uuid id PK
        uuid student_id FK
        uuid bus_id FK
        uuid route_id FK
        uuid pickup_stop_id FK
        uuid dropoff_stop_id FK
        string academic_year
        boolean is_active
    }

    Student {
        uuid id PK
        uuid parent_id FK
        string first_name
        string last_name
        string student_id_number UK
        string grade
        string section
        date date_of_birth
        string photo_url
        string current_status "OFF_BOARD | ON_BOARD | ABSENT"
        boolean is_active
    }

    FaceProfile {
        uuid id PK
        uuid student_id FK
        string model_version
        vector embedding "512-dim"
        float quality_score
        boolean is_active
        timestamp created_at
    }

    Attendance {
        uuid id PK
        uuid student_id FK
        uuid bus_id FK
        string event_type "BOARD | OFFBOARD | ABSENT | MANUAL"
        timestamp event_timestamp
        float confidence_score
        string verification_method "AI_FACE | MANUAL_OVERRIDE | NFC"
        string device_id
        float latitude
        float longitude
    }

    GPSEvent {
        uuid id PK
        uuid bus_id FK
        float latitude
        float longitude
        float speed
        float heading
        timestamp recorded_at
    }

    Alert {
        uuid id PK
        string alert_type "UNKNOWN_PERSON | ROUTE_DEVIATION | EMERGENCY | DEVICE_OFFLINE"
        string severity "LOW | MEDIUM | HIGH | CRITICAL"
        string status "OPEN | ACKNOWLEDGED | RESOLVED"
        uuid bus_id FK
        uuid student_id FK
        string description
        jsonb metadata
        timestamp created_at
    }

    Notification {
        uuid id PK
        uuid user_id FK
        string title
        string message
        string type "ATTENDANCE | LOCATION | SAFETY | SYSTEM"
        boolean is_read
        timestamp created_at
    }
```
