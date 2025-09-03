from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from app.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.services.flow_service import FlowService
from app.services.company_service import CompanyService
from app.schemas.flow import FlowCreate, FlowUpdate, FlowResponse
from app.models.onboarding_flow import OnboardingFlow

router = APIRouter()


@router.get("/", response_model=List[FlowResponse])
async def list_flows(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all onboarding flows for the current company"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    flows = db.query(OnboardingFlow).filter(
        OnboardingFlow.company_id == company.id
    ).all()
    
    return [
        FlowResponse(
            id=str(flow.id),
            name=flow.name,
            description=flow.description,
            duration_days=flow.duration_days,
            status=flow.status,
            company_id=str(flow.company_id),
            created_at=flow.created_at,
            updated_at=flow.updated_at
        )
        for flow in flows
    ]


@router.post("/", response_model=FlowResponse)
async def create_flow(
    flow_data: FlowCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new onboarding flow"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    result = FlowService.create_flow(db, str(company.id), flow_data.dict())
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    flow = result["flow"]
    return FlowResponse(
        id=str(flow.id),
        name=flow.name,
        description=flow.description,
        duration_days=flow.duration_days,
        status=flow.status,
        company_id=str(flow.company_id),
        created_at=flow.created_at,
        updated_at=flow.updated_at
    )


@router.get("/{flow_id}", response_model=FlowResponse)
async def get_flow(
    flow_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific onboarding flow"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    flow_uuid = uuid.UUID(flow_id)
    flow = db.query(OnboardingFlow).filter(
        OnboardingFlow.id == flow_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    return FlowResponse(
        id=str(flow.id),
        name=flow.name,
        description=flow.description,
        duration_days=flow.duration_days,
        status=flow.status,
        company_id=str(flow.company_id),
        created_at=flow.created_at,
        updated_at=flow.updated_at
    )


@router.patch("/{flow_id}", response_model=FlowResponse)
async def update_flow(
    flow_id: str,
    flow_data: FlowUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an onboarding flow"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify flow belongs to company
    flow_uuid = uuid.UUID(flow_id)
    flow = db.query(OnboardingFlow).filter(
        OnboardingFlow.id == flow_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    result = FlowService.update_flow(db, flow_id, flow_data.dict(exclude_unset=True))
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    updated_flow = result["flow"]
    return FlowResponse(
        id=str(updated_flow.id),
        name=updated_flow.name,
        description=updated_flow.description,
        duration_days=updated_flow.duration_days,
        status=updated_flow.status,
        company_id=str(updated_flow.company_id),
        created_at=updated_flow.created_at,
        updated_at=updated_flow.updated_at
    )


@router.delete("/{flow_id}")
async def delete_flow(
    flow_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an onboarding flow"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify flow belongs to company
    flow_uuid = uuid.UUID(flow_id)
    flow = db.query(OnboardingFlow).filter(
        OnboardingFlow.id == flow_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    db.delete(flow)
    db.commit()
    
    return {"message": "Flow deleted successfully"}


@router.get("/{flow_id}/pipeline")
async def get_flow_pipeline(
    flow_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get pipeline data for a flow"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify flow belongs to company
    flow_uuid = uuid.UUID(flow_id)
    flow = db.query(OnboardingFlow).filter(
        OnboardingFlow.id == flow_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    result = FlowService.get_pipeline_data(db, flow_id)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result["pipeline"]


@router.get("/{flow_id}/stats")
async def get_flow_stats(
    flow_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get statistics for a flow"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify flow belongs to company
    flow_uuid = uuid.UUID(flow_id)
    flow = db.query(OnboardingFlow).filter(
        OnboardingFlow.id == flow_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    result = FlowService.get_flow_stats(db, flow_id)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result["stats"] 