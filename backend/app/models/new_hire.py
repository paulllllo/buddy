from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid


class NewHire(Base):
    __tablename__ = "new_hires"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False, index=True)
    flow_id = Column(UUID(as_uuid=True), ForeignKey("onboarding_flows.id"), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    status = Column(String(20), default="pending")  # pending, started, completed, expired
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    session_token_expires_at = Column(DateTime, nullable=True, index=True)  # Token expiration
    invited_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="new_hires")
    flow = relationship("OnboardingFlow", back_populates="new_hires")
    progress = relationship("Progress", back_populates="new_hire", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<NewHire(id={self.id}, email='{self.email}', status='{self.status}')>"
    
    def is_session_token_expired(self) -> bool:
        """Check if session token is expired"""
        if not self.session_token_expires_at:
            return False  # No expiration set
        return datetime.utcnow() > self.session_token_expires_at
    
    def can_access_onboarding(self) -> bool:
        """Check if new hire can access onboarding"""
        return (
            self.status in ["pending", "started"] and 
            not self.is_session_token_expired()
        ) 