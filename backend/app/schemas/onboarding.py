from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import uuid
from .user_input import UserInputSubmission


class ContentBlockProgress(BaseModel):
    id: str
    type: str
    config: Dict[str, Any]
    content: Dict[str, Any]
    order_index: int
    status: str  # pending, in_progress, completed
    data: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    @field_validator('id', mode='before')
    @classmethod
    def convert_uuid_to_string(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True


class StageProgress(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    order: int
    type: Optional[str] = None
    status: str
    content_blocks: List[ContentBlockProgress] = []
    is_complete: bool
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    @field_validator('id', mode='before')
    @classmethod
    def convert_uuid_to_string(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True


class OnboardingSession(BaseModel):
    session_token: str
    new_hire_id: str
    flow_id: str
    flow_name: str
    company_name: str
    company_logo_url: Optional[str] = None
    new_hire_name: str
    new_hire_email: str
    status: str  # pending, active, completed
    current_stage_id: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    stages: List[StageProgress] = []
    
    @field_validator('new_hire_id', 'flow_id', 'current_stage_id', mode='before')
    @classmethod
    def convert_uuid_to_string(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True


class ProgressOverview(BaseModel):
    session_token: str
    new_hire_id: str
    flow_id: str
    total_stages: int
    completed_stages: int
    current_stage_id: Optional[str] = None
    current_stage_name: Optional[str] = None
    overall_progress_percentage: float
    started_at: Optional[datetime] = None
    estimated_completion_time: Optional[int] = None  # in minutes
    
    @field_validator('new_hire_id', 'flow_id', 'current_stage_id', mode='before')
    @classmethod
    def convert_uuid_to_string(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True


class ContentBlockCompletion(BaseModel):
    data: UserInputSubmission = Field(description="Collected data from the content block")


class StageCompletion(BaseModel):
    stage_id: str
    completed_at: datetime = Field(default_factory=datetime.utcnow)


class FileUpload(BaseModel):
    file_name: str
    file_size: int
    file_type: str
    file_url: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


class OnboardingStartRequest(BaseModel):
    pass  # No additional data needed for starting


class OnboardingCompleteRequest(BaseModel):
    feedback: Optional[str] = Field(None, description="Optional feedback from new hire")
    completion_notes: Optional[str] = Field(None, description="Any additional notes") 