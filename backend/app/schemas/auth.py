from typing import Optional
from pydantic import BaseModel, EmailStr, validator


class UserCreate(BaseModel):
    # User fields
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    
    # Company fields
    company_name: str
    company_industry: Optional[str] = None
    company_size: Optional[str] = None
    company_website: Optional[str] = None
    company_description: Optional[str] = None
    
    # Branding
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('primary_color', 'secondary_color', 'accent_color')
    def validate_color(cls, v):
        if v and not v.startswith('#'):
            raise ValueError('Color must be a valid hex color starting with #')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    company_id: str
    
    class Config:
        from_attributes = True 