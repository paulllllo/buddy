from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.models.content_block import JSONField
import uuid


class StageTemplate(Base):
    __tablename__ = "stage_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    type = Column(String(50), nullable=False)
    default_content = Column(JSONField)
    default_config = Column(JSONField)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<StageTemplate(id={self.id}, name='{self.name}', type='{self.type}')>" 