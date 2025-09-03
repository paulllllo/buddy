from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.services.stage_template_service import StageTemplateService
from app.schemas.content import (
    StageTemplateCreate,
    StageTemplateUpdate,
    StageTemplateResponse
)

router = APIRouter()


@router.get("/", response_model=List[StageTemplateResponse])
async def list_stage_templates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all available stage templates"""
    templates = StageTemplateService.get_all_templates(db)
    return templates


@router.get("/{template_id}", response_model=StageTemplateResponse)
async def get_stage_template(
    template_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific stage template"""
    template = StageTemplateService.get_template_by_id(db, template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="Stage template not found")
    
    return template


@router.get("/type/{template_type}", response_model=List[StageTemplateResponse])
async def get_templates_by_type(
    template_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get stage templates by type"""
    templates = StageTemplateService.get_templates_by_type(db, template_type)
    return templates


@router.post("/", response_model=StageTemplateResponse)
async def create_stage_template(
    template_data: StageTemplateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new stage template"""
    template = StageTemplateService.create_template(
        db=db,
        name=template_data.name,
        description=template_data.description,
        template_type=template_data.type,
        default_content=template_data.default_content,
        default_config=template_data.default_config,
        is_public=template_data.is_public
    )
    
    return template


@router.put("/{template_id}", response_model=StageTemplateResponse)
async def update_stage_template(
    template_id: str,
    template_data: StageTemplateUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a stage template"""
    template = StageTemplateService.get_template_by_id(db, template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="Stage template not found")
    
    # Update fields
    if template_data.name is not None:
        template.name = template_data.name
    if template_data.description is not None:
        template.description = template_data.description
    if template_data.type is not None:
        template.type = template_data.type
    if template_data.default_content is not None:
        template.default_content = template_data.default_content
    if template_data.default_config is not None:
        template.default_config = template_data.default_config
    if template_data.is_public is not None:
        template.is_public = template_data.is_public
    
    db.commit()
    db.refresh(template)
    
    return template


@router.delete("/{template_id}")
async def delete_stage_template(
    template_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a stage template"""
    template = StageTemplateService.get_template_by_id(db, template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="Stage template not found")
    
    db.delete(template)
    db.commit()
    
    return {"message": "Stage template deleted successfully"} 