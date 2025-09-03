from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from app.database import get_db
from app.models.user import User
from app.models.stage import Stage
from app.models.onboarding_flow import OnboardingFlow
from app.auth.dependencies import get_current_user
from app.services.content_service import ContentService
from app.schemas.content import (
    ContentBlockCreate,
    ContentBlockUpdate,
    ContentBlockResponse,
    ContentBlockReorder
)

router = APIRouter()


@router.get("/stages/{stage_id}/content-blocks", response_model=List[ContentBlockResponse])
async def list_content_blocks(
    stage_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all content blocks for a stage"""
    # Verify stage belongs to user's company
    stage_uuid = uuid.UUID(stage_id)
    stage = db.query(Stage).join(OnboardingFlow).filter(
        Stage.id == stage_uuid,
        OnboardingFlow.company_id == current_user.company_id
    ).first()
    
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    
    content_blocks = ContentService.get_content_blocks_by_stage(db, stage_id)
    return content_blocks


@router.post("/stages/{stage_id}/content-blocks", response_model=ContentBlockResponse)
async def create_content_block(
    stage_id: str,
    content_block_data: ContentBlockCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new content block in a stage"""
    # Verify stage belongs to user's company
    stage_uuid = uuid.UUID(stage_id)
    stage = db.query(Stage).join(OnboardingFlow).filter(
        Stage.id == stage_uuid,
        OnboardingFlow.company_id == current_user.company_id
    ).first()
    
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    
    try:
        content_block = ContentService.create_content_block(
            db=db,
            stage_id=stage_id,
            content_type_name=content_block_data.type,
            config=content_block_data.config,
            content=content_block_data.content,
            order_index=content_block_data.order_index
        )
        return content_block
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/content-blocks/{content_block_id}", response_model=ContentBlockResponse)
async def get_content_block(
    content_block_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific content block"""
    content_block = ContentService.get_content_block(db, content_block_id)
    
    if not content_block:
        raise HTTPException(status_code=404, detail="Content block not found")
    
    # Verify content block belongs to user's company
    stage_uuid = uuid.UUID(str(content_block.stage_id))
    stage = db.query(Stage).join(OnboardingFlow).filter(
        Stage.id == stage_uuid,
        OnboardingFlow.company_id == current_user.company_id
    ).first()
    
    if not stage:
        raise HTTPException(status_code=404, detail="Content block not found")
    
    return content_block


@router.put("/content-blocks/{content_block_id}", response_model=ContentBlockResponse)
async def update_content_block(
    content_block_id: str,
    content_block_data: ContentBlockUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a content block"""
    # Verify content block belongs to user's company
    content_block = ContentService.get_content_block(db, content_block_id)
    if not content_block:
        raise HTTPException(status_code=404, detail="Content block not found")
    
    # content_block.stage_id is already a UUID object from SQLAlchemy
    stage = db.query(Stage).join(OnboardingFlow).filter(
        Stage.id == content_block.stage_id,
        OnboardingFlow.company_id == current_user.company_id
    ).first()
    
    if not stage:
        raise HTTPException(status_code=404, detail="Content block not found")
    
    updated_block = ContentService.update_content_block(
        db=db,
        content_block_id=content_block_id,
        config=content_block_data.config,
        content=content_block_data.content
    )
    
    if not updated_block:
        raise HTTPException(status_code=404, detail="Content block not found")
    
    return updated_block


@router.delete("/content-blocks/{content_block_id}")
async def delete_content_block(
    content_block_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a content block"""
    # Verify content block belongs to user's company
    content_block = ContentService.get_content_block(db, content_block_id)
    if not content_block:
        raise HTTPException(status_code=404, detail="Content block not found")
    
    # content_block.stage_id is already a UUID object from SQLAlchemy
    stage = db.query(Stage).join(OnboardingFlow).filter(
        Stage.id == content_block.stage_id,
        OnboardingFlow.company_id == current_user.company_id
    ).first()
    
    if not stage:
        raise HTTPException(status_code=404, detail="Content block not found")
    
    success = ContentService.delete_content_block(db, content_block_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Content block not found")
    
    return {"message": "Content block deleted successfully"}


@router.post("/stages/{stage_id}/content-blocks/reorder", response_model=List[ContentBlockResponse])
async def reorder_content_blocks(
    stage_id: str,
    reorder_data: ContentBlockReorder,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reorder content blocks within a stage"""
    # Verify stage belongs to user's company
    stage_uuid = uuid.UUID(stage_id)
    stage = db.query(Stage).join(OnboardingFlow).filter(
        Stage.id == stage_uuid,
        OnboardingFlow.company_id == current_user.company_id
    ).first()
    
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    
    content_blocks = ContentService.reorder_content_blocks(
        db=db,
        stage_id=stage_id,
        content_block_orders=reorder_data.content_blocks
    )
    
    return content_blocks 