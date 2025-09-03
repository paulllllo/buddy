from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
import uuid


class CompanyBase(BaseModel):
    name: str
    industry: Optional[str] = None
    size: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    primary_color: Optional[str] = "#3B82F6"
    secondary_color: Optional[str] = "#1F2937"
    accent_color: Optional[str] = "#10B981"


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: str
    logo_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    @field_validator('id', mode='before')
    @classmethod
    def convert_uuid_to_string(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True 