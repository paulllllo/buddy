from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
import json

# Abstract JSON field for both SQLite and PostgreSQL
import json
from sqlalchemy import Text
from sqlalchemy.types import TypeDecorator

class JSONField(TypeDecorator):
    """JSON field that works with both SQLite and PostgreSQL"""
    impl = Text
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None
    
    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return None


class ContentBlock(Base):
    __tablename__ = "content_blocks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stage_id = Column(UUID(as_uuid=True), ForeignKey("stages.id"), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)  # content type name (header, description, etc.)
    config = Column(JSONField, nullable=False)  # validation and display configuration
    content = Column(JSONField, nullable=False)  # actual content data
    order_index = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stage = relationship("Stage", back_populates="content_blocks")
    progress = relationship("Progress", back_populates="content_block")

    def __repr__(self):
        return f"<ContentBlock(id={self.id}, type='{self.type}', stage_id={self.stage_id}, order={self.order_index})>" 