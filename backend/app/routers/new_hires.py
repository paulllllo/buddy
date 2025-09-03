from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from app.database import get_db
from app.models.user import User
from app.models.new_hire import NewHire
from app.models.onboarding_flow import OnboardingFlow
from app.auth.dependencies import get_current_user
from app.services.new_hire_service import NewHireService
from app.services.company_service import CompanyService
from app.schemas.new_hire import NewHireCreate, NewHireUpdate, NewHireResponse
from app.schemas.new_hire import StatusUpdate
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=List[NewHireResponse])
async def list_new_hires(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all new hires for the current company"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    new_hires = NewHireService.get_new_hires_by_company(db, str(company.id))
    
    return [
        NewHireResponse(
            id=str(nh.id),
            email=nh.email,
            first_name=nh.first_name,
            last_name=nh.last_name,
            status=nh.status,
            invited_at=nh.invited_at,
            started_at=nh.started_at,
            completed_at=nh.completed_at,
            flow_id=str(nh.flow_id),
            company_id=str(nh.company_id),
            session_token=nh.session_token,
            session_token_expires_at=nh.session_token_expires_at,
            created_at=nh.created_at
        )
        for nh in new_hires
    ]


@router.post("/", response_model=NewHireResponse)
async def create_new_hire(
    new_hire_data: NewHireCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new hire"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify flow belongs to user's company
    flow_uuid = uuid.UUID(new_hire_data.flow_id)
    flow = db.query(OnboardingFlow).filter(
        OnboardingFlow.id == flow_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    # Check if new hire already exists with this email
    existing = db.query(NewHire).filter(
        NewHire.email == new_hire_data.email,
        NewHire.company_id == company.id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="New hire with this email already exists")
    
    result = NewHireService.create_new_hire(db, str(company.id), new_hire_data.dict())
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error creating new hire"])
    
    new_hire = result["new_hire"]
    return NewHireResponse(
        id=str(new_hire.id),
        email=new_hire.email,
        first_name=new_hire.first_name,
        last_name=new_hire.last_name,
        status=new_hire.status,
        invited_at=new_hire.invited_at,
        started_at=new_hire.started_at,
        completed_at=new_hire.completed_at,
        flow_id=str(new_hire.flow_id),
        company_id=str(new_hire.company_id),
        session_token=new_hire.session_token,  # Include session token in response
        session_token_expires_at=new_hire.session_token_expires_at,
        created_at=new_hire.created_at
    )


@router.get("/{new_hire_id}", response_model=NewHireResponse)
async def get_new_hire(
    new_hire_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific new hire"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    new_hire_uuid = uuid.UUID(new_hire_id)
    new_hire = db.query(NewHire).join(OnboardingFlow).filter(
        NewHire.id == new_hire_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not new_hire:
        raise HTTPException(status_code=404, detail="New hire not found")
    
    return NewHireResponse(
        id=str(new_hire.id),
        email=new_hire.email,
        first_name=new_hire.first_name,
        last_name=new_hire.last_name,
        status=new_hire.status,
        invited_at=new_hire.invited_at,
        session_token=new_hire.session_token,
        session_token_expires_at=new_hire.session_token_expires_at,
        started_at=new_hire.started_at,
        completed_at=new_hire.completed_at,
        flow_id=str(new_hire.flow_id),
        company_id=str(new_hire.company_id),
        created_at=new_hire.created_at,
        updated_at=new_hire.updated_at if hasattr(new_hire, 'updated_at') else None
    )


@router.patch("/{new_hire_id}", response_model=NewHireResponse)
async def update_new_hire(
    new_hire_id: str,
    new_hire_data: NewHireUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a new hire"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    new_hire_uuid = uuid.UUID(new_hire_id)
    new_hire = db.query(NewHire).join(OnboardingFlow).filter(
        NewHire.id == new_hire_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not new_hire:
        raise HTTPException(status_code=404, detail="New hire not found")
    
    # Update allowed fields
    allowed_fields = ["first_name", "last_name", "status"]
    
    for field, value in new_hire_data.dict(exclude_unset=True).items():
        if field in allowed_fields and hasattr(new_hire, field):
            setattr(new_hire, field, value)
    
    db.commit()
    db.refresh(new_hire)
    
    return NewHireResponse(
        id=str(new_hire.id),
        email=new_hire.email,
        first_name=new_hire.first_name,
        last_name=new_hire.last_name,
        status=new_hire.status,
        invited_at=new_hire.invited_at,
        started_at=new_hire.started_at,
        completed_at=new_hire.completed_at,
        flow_id=str(new_hire.flow_id),
        company_id=str(new_hire.company_id),
        created_at=new_hire.created_at
    )


@router.delete("/{new_hire_id}")
async def delete_new_hire(
    new_hire_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a new hire"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    new_hire_uuid = uuid.UUID(new_hire_id)
    new_hire = db.query(NewHire).join(OnboardingFlow).filter(
        NewHire.id == new_hire_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not new_hire:
        raise HTTPException(status_code=404, detail="New hire not found")
    
    db.delete(new_hire)
    db.commit()
    
    return {"message": "New hire deleted successfully"}


@router.get("/{new_hire_id}/progress")
async def get_new_hire_progress(
    new_hire_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get progress for a specific new hire"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify new hire belongs to company
    new_hire_uuid = uuid.UUID(new_hire_id)
    new_hire = db.query(NewHire).join(OnboardingFlow).filter(
        NewHire.id == new_hire_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not new_hire:
        raise HTTPException(status_code=404, detail="New hire not found")
    
    result = NewHireService.get_progress(db, new_hire_id)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result["progress"]


@router.post("/{new_hire_id}/resend-invitation")
async def resend_invitation(
    new_hire_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Resend invitation to a new hire"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Verify new hire belongs to company
    new_hire_uuid = uuid.UUID(new_hire_id)
    new_hire = db.query(NewHire).join(OnboardingFlow).filter(
        NewHire.id == new_hire_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not new_hire:
        raise HTTPException(status_code=404, detail="New hire not found")
    
    result = NewHireService.resend_invitation(db, new_hire_id)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {
        "message": "Invitation resent successfully",
        "session_token": result["session_token"]
    }


async def update_new_hire_status(
    new_hire_id: str,
    status_data: StatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update new hire status"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    new_hire_uuid = uuid.UUID(new_hire_id)
    new_hire = db.query(NewHire).join(OnboardingFlow).filter(
        NewHire.id == new_hire_uuid,
        OnboardingFlow.company_id == company.id
    ).first()
    
    if not new_hire:
        raise HTTPException(status_code=404, detail="New hire not found")
    
    new_status = status_data.status
    if new_status not in ["pending", "started", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    new_hire.status = new_status
    
    if new_status == "started" and not new_hire.started_at:
        new_hire.started_at = datetime.utcnow()
    elif new_status == "completed" and not new_hire.completed_at:
        new_hire.completed_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Status updated successfully"} 