from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.services.content_type_service import ContentTypeService
from app.services.content_service import ContentService
from app.schemas.content import (
    ContentTypeResponse, 
    ContentValidationRequest, 
    ContentValidationResponse
)

router = APIRouter()


@router.get("/", response_model=List[ContentTypeResponse])
async def list_content_types(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all available content types"""
    content_types = ContentTypeService.get_all_content_types(db)
    return content_types


@router.get("/{name}", response_model=ContentTypeResponse)
async def get_content_type(
    name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific content type by name"""
    content_type = ContentTypeService.get_content_type_by_name(db, name)
    
    if not content_type:
        raise HTTPException(status_code=404, detail="Content type not found")
    
    return content_type


@router.get("/{name}/config")
async def get_content_type_config(
    name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the default configuration for a content type"""
    content_type = ContentTypeService.get_content_type_by_name(db, name)
    
    if not content_type:
        raise HTTPException(status_code=404, detail="Content type not found")
    
    return {
        "name": content_type.name,
        "display_name": content_type.display_name,
        "default_config": content_type.default_config
    }


@router.post("/validate", response_model=ContentValidationResponse)
async def validate_content(
    validation_data: ContentValidationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Validate content against a content type"""
    validation_result = ContentService.validate_content_block(
        db,
        validation_data.type,
        validation_data.config,
        validation_data.content
    )
    
    return ContentValidationResponse(
        valid=validation_result["valid"],
        errors=validation_result.get("errors", []),
        content_type=validation_data.type
    ) 