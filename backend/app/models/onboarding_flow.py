from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid


class OnboardingFlow(Base):
    __tablename__ = "onboarding_flows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    duration_days = Column(Integer)
    status = Column(String(20), default="draft")  # draft, published, archived
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="onboarding_flows")
    stages = relationship("Stage", back_populates="flow", cascade="all, delete-orphan", order_by="Stage.order")
    new_hires = relationship("NewHire", back_populates="flow")

    def __repr__(self):
        return f"<OnboardingFlow(id={self.id}, name='{self.name}', company_id={self.company_id})>" 