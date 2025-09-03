from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid


class Stage(Base):
    __tablename__ = "stages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flow_id = Column(UUID(as_uuid=True), ForeignKey("onboarding_flows.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    order = Column(Integer, nullable=False, index=True)
    type = Column(String(50))  # text, media, form, etc.
    status = Column(String(20), default="active")  # active, inactive
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    flow = relationship("OnboardingFlow", back_populates="stages")
    content_blocks = relationship("ContentBlock", back_populates="stage", cascade="all, delete-orphan", order_by="ContentBlock.order_index")
    progress = relationship("Progress", back_populates="stage")

    def __repr__(self):
        return f"<Stage(id={self.id}, name='{self.name}', flow_id={self.flow_id}, order={self.order})>" 