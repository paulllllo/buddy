from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.services.company_service import CompanyService
from app.schemas.company import CompanyUpdate, CompanyResponse

router = APIRouter()


@router.get("/me", response_model=CompanyResponse)
async def get_company_info(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Get current user's company information"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return CompanyResponse(
        id=str(company.id),
        name=company.name,
        industry=company.industry,
        size=company.size,
        website=company.website,
        description=company.description,
        primary_color=company.primary_color,
        secondary_color=company.secondary_color,
        accent_color=company.accent_color,
        logo_url=company.logo_url,
        created_at=company.created_at,
        updated_at=company.updated_at
    )


@router.patch("/me", response_model=CompanyResponse)
async def update_company_info(
    company_data: CompanyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's company information"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    result = CompanyService.update_company(db, str(company.id), company_data.dict(exclude_unset=True))
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    updated_company = result["company"]
    return CompanyResponse(
        id=str(updated_company.id),
        name=updated_company.name,
        industry=updated_company.industry,
        size=updated_company.size,
        website=updated_company.website,
        description=updated_company.description,
        primary_color=updated_company.primary_color,
        secondary_color=updated_company.secondary_color,
        accent_color=updated_company.accent_color,
        logo_url=updated_company.logo_url,
        created_at=updated_company.created_at,
        updated_at=updated_company.updated_at
    )


@router.post("/me/logo")
async def upload_company_logo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload company logo"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    result = CompanyService.upload_logo(db, str(company.id), file)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return {
        "message": "Logo uploaded successfully",
        "logo_url": result["logo_url"]
    }


@router.get("/me/stats")
async def get_company_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get company statistics and analytics"""
    company = CompanyService.get_company_by_user_id(db, str(current_user.id))
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    result = CompanyService.get_company_stats(db, str(company.id))
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result["stats"] 