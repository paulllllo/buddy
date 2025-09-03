from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import datetime
import uuid


class NewHireBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    flow_id: str


class NewHireCreate(NewHireBase):
    pass


class NewHireUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[str] = None


class NewHireResponse(NewHireBase):
    id: str
    company_id: str
    status: str
    invited_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    session_token: Optional[str] = None  # Include session token for admin access
    session_token_expires_at: Optional[datetime] = None  # Optional for admin access
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    @field_validator('id', 'company_id', 'flow_id', mode='before')
    @classmethod
    def convert_uuid_to_string(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True


class StatusUpdate(BaseModel):
    status: str = Field(..., description="The status of the new hire")

