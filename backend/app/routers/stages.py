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
from app.services.flow_service import FlowService
from app.services.company_service import CompanyService
from app.schemas.stage import StageCreate, StageUpdate, StageResponse

router = APIRouter()


@router.get("/flows/{flow_id}/stages", response_model=List[StageResponse])
async def list_stages(
    flow_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all stages for a specific flow"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify flow belongs to user's company
    flow_uuid = uuid.UUID(flow_id)
    flow = db.query(OnboardingFlow).filter(
        OnboardingFlow.id == flow_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    stages = db.query(Stage).filter(Stage.flow_id == flow_uuid).order_by(Stage.order).all()
    
    result = []
    for stage in stages:
        # Get content blocks for this stage
        content_blocks = ContentService.get_content_blocks_by_stage(db, str(stage.id))
        
        result.append(StageResponse(
            id=str(stage.id),
            name=stage.name,
            description=stage.description,
            order=stage.order,
            type=stage.type,
            status=stage.status,
            flow_id=str(stage.flow_id),
            created_at=stage.created_at,
            content_blocks=[
                {
                    "id": str(cb.id),
                    "type": cb.type,
                    "config": cb.config,
                    "content": cb.content,
                    "order_index": cb.order_index
                }
                for cb in content_blocks
            ]
        ))
    
    return result


@router.post("/flows/{flow_id}/stages", response_model=StageResponse)
async def create_stage(
    flow_id: str,
    stage_data: StageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new stage in a flow"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify flow belongs to user's company
    flow_uuid = uuid.UUID(flow_id)
    flow = db.query(OnboardingFlow).filter(
        OnboardingFlow.id == flow_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    result = FlowService.add_stage(db, flow_id, stage_data.dict())
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    stage = result["stage"]
    return StageResponse(
        id=str(stage.id),
        name=stage.name,
        description=stage.description,
        order=stage.order,
        type=stage.type,
        status=stage.status,
        flow_id=str(stage.flow_id),
        created_at=stage.created_at,
        content_blocks=[]
    )


@router.post("/flows/{flow_id}/stages/template/{template_id}", response_model=StageResponse)
async def create_stage_from_template(
    flow_id: str,
    template_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new stage in a flow using a stage template"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify flow belongs to user's company
    flow_uuid = uuid.UUID(flow_id)
    flow = db.query(OnboardingFlow).filter(
        OnboardingFlow.id == flow_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    # Get the stage template
    template_uuid = uuid.UUID(template_id)
    from app.models.stage_template import StageTemplate
    template = db.query(StageTemplate).filter(StageTemplate.id == template_uuid).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Stage template not found")
    
    # Create stage data from template
    stage_data = {
        "name": template.name,
        "description": template.description,
        "type": template.type
    }
    
    # Create the stage with template
    result = FlowService.add_stage(db, flow_id, stage_data, template_id)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    stage = result["stage"]
    
    # Get the created content blocks
    content_blocks = ContentService.get_content_blocks_by_stage(db, str(stage.id))
    
    return StageResponse(
        id=str(stage.id),
        name=stage.name,
        description=stage.description,
        order=stage.order,
        type=stage.type,
        status=stage.status,
        flow_id=str(stage.flow_id),
        created_at=stage.created_at,
        content_blocks=[
            {
                "id": str(cb.id),
                "type": cb.type,
                "config": cb.config,
                "content": cb.content,
                "order_index": cb.order_index
            }
            for cb in content_blocks
        ]
    )


@router.get("/flows/{flow_id}/stages/{stage_id}", response_model=StageResponse)
async def get_stage(
    flow_id: str,
    stage_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific stage"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify flow belongs to user's company
    flow_uuid = uuid.UUID(flow_id)
    stage_uuid = uuid.UUID(stage_id)
    flow = db.query(OnboardingFlow).filter(
        OnboardingFlow.id == flow_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    stage = db.query(Stage).filter(
        Stage.id == stage_uuid,
        Stage.flow_id == flow_uuid
    ).first()
    
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    
    # Get content blocks for this stage
    content_blocks = ContentService.get_content_blocks_by_stage(db, str(stage.id))
    
    return StageResponse(
        id=str(stage.id),
        name=stage.name,
        description=stage.description,
        order=stage.order,
        type=stage.type,
        status=stage.status,
        flow_id=str(stage.flow_id),
        created_at=stage.created_at,
        content_blocks=[
            {
                "id": str(cb.id),
                "type": cb.type,
                "config": cb.config,
                "content": cb.content,
                "order_index": cb.order_index
            }
            for cb in content_blocks
        ]
    )


@router.patch("/flows/{flow_id}/stages/{stage_id}", response_model=StageResponse)
async def update_stage(
    flow_id: str,
    stage_id: str,
    stage_data: StageUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a stage"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify flow belongs to user's company
    flow_uuid = uuid.UUID(flow_id)
    flow = db.query(OnboardingFlow).filter(
        OnboardingFlow.id == flow_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    result = FlowService.update_stage(db, flow_id, stage_id, stage_data.dict(exclude_unset=True))
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    stage = result["stage"]
    # Get content blocks for this stage
    content_blocks = ContentService.get_content_blocks_by_stage(db, str(stage.id))
    
    return StageResponse(
        id=str(stage.id),
        name=stage.name,
        description=stage.description,
        order=stage.order,
        type=stage.type,
        status=stage.status,
        flow_id=str(stage.flow_id),
        created_at=stage.created_at,
        content_blocks=[
            {
                "id": str(cb.id),
                "type": cb.type,
                "config": cb.config,
                "content": cb.content,
                "order_index": cb.order_index
            }
            for cb in content_blocks
        ]
    )


@router.delete("/flows/{flow_id}/stages/{stage_id}")
async def delete_stage(
    flow_id: str,
    stage_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a stage"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify flow belongs to user's company
    flow_uuid = uuid.UUID(flow_id)
    stage_uuid = uuid.UUID(stage_id)
    flow = db.query(OnboardingFlow).filter(
        OnboardingFlow.id == flow_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    stage = db.query(Stage).filter(
        Stage.id == stage_uuid,
        Stage.flow_id == flow_uuid
    ).first()
    
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    
    db.delete(stage)
    db.commit()
    
    return {"message": "Stage deleted successfully"}


@router.patch("/flows/{flow_id}/stages/reorder")
async def reorder_stages(
    flow_id: str,
    stage_order: List[str],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reorder stages in a flow"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify flow belongs to user's company
    flow_uuid = uuid.UUID(flow_id)
    flow = db.query(OnboardingFlow).filter(
        OnboardingFlow.id == flow_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    result = FlowService.reorder_stages(db, flow_id, stage_order)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {"message": "Stages reordered successfully"} 