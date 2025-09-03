from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.content_block import JSONField
import uuid


class Progress(Base):
    __tablename__ = "progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    new_hire_id = Column(UUID(as_uuid=True), ForeignKey("new_hires.id"), nullable=False, index=True)
    stage_id = Column(UUID(as_uuid=True), ForeignKey("stages.id"), nullable=False, index=True)
    content_block_id = Column(UUID(as_uuid=True), ForeignKey("content_blocks.id"), nullable=False, index=True)
    status = Column(String(20), default="pending")  # pending, in_progress, completed
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    data = Column(JSONField)  # Form submissions, responses
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    new_hire = relationship("NewHire", back_populates="progress")
    stage = relationship("Stage", back_populates="progress")
    content_block = relationship("ContentBlock", back_populates="progress")

    def __repr__(self):
        return f"<Progress(id={self.id}, new_hire_id={self.new_hire_id}, content_block_id={self.content_block_id}, status='{self.status}')>" 