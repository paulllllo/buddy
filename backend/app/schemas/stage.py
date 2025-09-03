from typing import Optional, List, Dict, Any
from pydantic import BaseModel, field_validator
from datetime import datetime
import uuid


class StageBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: Optional[str] = None


class StageCreate(StageBase):
    pass


class StageUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None


class StageResponse(StageBase):
    id: str
    flow_id: str
    order: int
    status: str
    created_at: datetime
    content_blocks: List[Dict[str, Any]] = []
    
    @field_validator('id', 'flow_id', mode='before')
    @classmethod
    def convert_uuid_to_string(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True 