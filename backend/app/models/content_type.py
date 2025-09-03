from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.models.content_block import JSONField
import uuid


class ContentType(Base):
    __tablename__ = "content_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False, index=True)  # header, description, etc.
    display_name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # form, media, text, etc.
    default_config = Column(JSONField)  # default validation and display rules
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ContentType(id={self.id}, name='{self.name}', display_name='{self.display_name}')>" 