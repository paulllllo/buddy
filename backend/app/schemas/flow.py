from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
import uuid


class FlowBase(BaseModel):
    name: str
    description: Optional[str] = None
    duration_days: Optional[int] = None
    status: Optional[str] = "draft"


class FlowCreate(FlowBase):
    pass


class FlowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_days: Optional[int] = None
    status: Optional[str] = None


class FlowResponse(FlowBase):
    id: str
    company_id: str
    created_at: datetime
    updated_at: datetime
    
    @field_validator('id', 'company_id', mode='before')
    @classmethod
    def convert_uuid_to_string(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True 