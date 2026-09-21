from sqlalchemy import Column, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from app.core.database import Base
from app.models.base import TimestampMixin

class FaceProfile(TimestampMixin, Base):
    __tablename__ = "face_profiles"

    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    model_version = Column(String, nullable=False, default="v1")
    embedding = Column(Vector(512), nullable=False) # 512-dim embedding for InsightFace etc.
    quality_score = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)

    student = relationship("Student", back_populates="face_profiles")
