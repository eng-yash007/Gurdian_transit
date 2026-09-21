import asyncio
import sys
import os
import random
from datetime import datetime, timezone, timedelta
from faker import Faker
from passlib.context import CryptContext

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app.core.database import AsyncSessionLocal
from app.models.user import User, Parent, Driver
from app.models.student import Student
from app.models.fleet import Bus, Route, BusStop, BusAssignment
from app.models.face_profile import FaceProfile

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake = Faker()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def seed_data():
    async with AsyncSessionLocal() as db:
        print("Creating Admin User...")
        admin = User(
            email="admin@school.com",
            hashed_password=get_password_hash("password123"),
            role="ADMIN",
            full_name="School Administrator"
        )
        db.add(admin)
        
        print("Creating Driver...")
        driver_user = User(
            email="driver1@school.com",
            hashed_password=get_password_hash("password123"),
            role="DRIVER",
            full_name=fake.name()
        )
        db.add(driver_user)
        await db.flush()
        
        driver = Driver(
            user_id=driver_user.id,
            license_number=fake.bothify(text='DL-########')
        )
        db.add(driver)
        
        print("Creating Bus...")
        bus = Bus(
            bus_number="BUS-101",
            license_plate=fake.license_plate(),
            capacity=40,
            current_driver_id=driver.id
        )
        db.add(bus)
        
        print("Creating Route...")
        route = Route(
            name="Morning Route A",
            start_point="City Center",
            end_point="School Campus"
        )
        db.add(route)
        await db.flush()
        
        print("Creating Parents and Students...")
        parent_user = User(
            email="parent1@school.com",
            hashed_password=get_password_hash("password123"),
            role="PARENT",
            full_name=fake.name(),
            phone_number=fake.phone_number()
        )
        db.add(parent_user)
        await db.flush()
        
        parent = Parent(
            user_id=parent_user.id,
            emergency_contact=fake.phone_number(),
            address=fake.address()
        )
        db.add(parent)
        await db.flush()
        
        student = Student(
            parent_id=parent.id,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            student_id_number=fake.bothify(text='STU-#####'),
            grade="10th",
            section="A"
        )
        db.add(student)
        await db.flush()
        
        print("Creating Bus Assignment...")
        assignment = BusAssignment(
            student_id=student.id,
            bus_id=bus.id,
            route_id=route.id,
            academic_year="2026-2027"
        )
        db.add(assignment)
        
        print("Creating Face Profile...")
        face_profile = FaceProfile(
            student_id=student.id,
            model_version="insightface_v1",
            embedding=[random.uniform(-1, 1) for _ in range(512)],
            quality_score=0.95
        )
        db.add(face_profile)
        
        await db.commit()
        print("Seed data successfully added!")

if __name__ == "__main__":
    print("Starting database seeding...")
    asyncio.run(seed_data())
