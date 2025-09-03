from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from app.models.company import Company
from app.models.user import User
from app.models.onboarding_flow import OnboardingFlow
from app.models.new_hire import NewHire
from app.storage.factory import get_storage
from app.auth.jwt import get_password_hash


class CompanyService:
    """Service for managing companies and related operations"""
    
    @staticmethod
    def create_company(db: Session, company_data: dict, admin_data: dict) -> Dict[str, Any]:
        """Create a new company with an admin user"""
        try:
            # Create company
            company = Company(
                name=company_data["name"],
                industry=company_data.get("industry"),
                size=company_data.get("size"),
                website=company_data.get("website"),
                description=company_data.get("description"),
                primary_color=company_data.get("primary_color", "#3B82F6"),
                secondary_color=company_data.get("secondary_color", "#1F2937"),
                accent_color=company_data.get("accent_color", "#10B981")
            )
            db.add(company)
            db.flush()  # Get the company ID
            
            # Create admin user
            admin_user = User(
                company_id=company.id,
                email=admin_data["email"],
                first_name=admin_data["first_name"],
                last_name=admin_data["last_name"],
                password_hash=get_password_hash(admin_data["password"]),
                role="admin"
            )
            db.add(admin_user)
            
            db.commit()
            
            return {
                "success": True,
                "company_id": str(company.id),
                "user_id": str(admin_user.id)
            }
            
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def update_company(db: Session, company_id: str, data: dict) -> Dict[str, Any]:
        """Update company information"""
        try:
            company_uuid = uuid.UUID(company_id)
            company = db.query(Company).filter(Company.id == company_uuid).first()
            
            if not company:
                return {"success": False, "error": "Company not found"}
            
            # Update fields
            for field, value in data.items():
                if hasattr(company, field) and value is not None:
                    setattr(company, field, value)
            
            company.updated_at = datetime.utcnow()
            db.commit()
            
            return {"success": True, "company": company}
            
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def upload_logo(db: Session, company_id: str, file) -> Dict[str, Any]:
        """Upload company logo"""
        try:
            company_uuid = uuid.UUID(company_id)
            company = db.query(Company).filter(Company.id == company_uuid).first()
            
            if not company:
                return {"success": False, "error": "Company not found"}
            
            # Get storage service
            storage = get_storage()
            
            # Generate file path
            file_path = f"companies/{company_id}/logo/{file.filename}"
            
            # Upload file
            file_url = storage.upload_file(file, file_path)
            
            # Update company logo URL
            company.logo_url = file_url
            company.updated_at = datetime.utcnow()
            
            db.commit()
            
            return {
                "success": True,
                "logo_url": file_url
            }
            
        except Exception as e:
            db.rollback()
            return {"success": False, "error": f"Logo upload failed: {str(e)}"}
    
    @staticmethod
    def get_company_stats(db: Session, company_id: str) -> Dict[str, Any]:
        """Get company statistics and analytics"""
        try:
            company_uuid = uuid.UUID(company_id)
            company = db.query(Company).filter(Company.id == company_uuid).first()
            
            if not company:
                return {"success": False, "error": "Company not found"}
            
            # Count onboarding flows
            total_flows = db.query(OnboardingFlow).filter(
                OnboardingFlow.company_id == company_uuid
            ).count()
            
            published_flows = db.query(OnboardingFlow).filter(
                OnboardingFlow.company_id == company_uuid,
                OnboardingFlow.status == "published"
            ).count()
            
            # Count new hires
            total_new_hires = db.query(NewHire).filter(
                NewHire.company_id == company_uuid
            ).count()
            
            active_new_hires = db.query(NewHire).filter(
                NewHire.company_id == company_uuid,
                NewHire.status == "started"
            ).count()
            
            completed_new_hires = db.query(NewHire).filter(
                NewHire.company_id == company_uuid,
                NewHire.status == "completed"
            ).count()
            
            # Count users
            total_users = db.query(User).filter(
                User.company_id == company_uuid
            ).count()
            
            active_users = db.query(User).filter(
                User.company_id == company_uuid,
                User.is_active == True
            ).count()
            
            return {
                "success": True,
                "stats": {
                    "company": {
                        "name": company.name,
                        "industry": company.industry,
                        "size": company.size,
                        "created_at": company.created_at
                    },
                    "onboarding_flows": {
                        "total": total_flows,
                        "published": published_flows,
                        "draft": total_flows - published_flows
                    },
                    "new_hires": {
                        "total": total_new_hires,
                        "active": active_new_hires,
                        "completed": completed_new_hires,
                        "pending": total_new_hires - active_new_hires - completed_new_hires
                    },
                    "users": {
                        "total": total_users,
                        "active": active_users,
                        "inactive": total_users - active_users
                    }
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_company_by_id(db: Session, company_id: str) -> Optional[Company]:
        """Get company by ID"""
        try:
            company_uuid = uuid.UUID(company_id)
            return db.query(Company).filter(Company.id == company_uuid).first()
        except ValueError:
            return None
    
    @staticmethod
    def get_company_by_user_id(db: Session, user_id: str) -> Optional[Company]:
        """Get company by user ID"""
        try:
            user_uuid = uuid.UUID(user_id)
            user = db.query(User).filter(User.id == user_uuid).first()
            if user:
                return db.query(Company).filter(Company.id == user.company_id).first()
            return None
        except ValueError:
            return None 