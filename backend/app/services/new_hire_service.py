from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
import secrets
from app.models.new_hire import NewHire
from app.models.stage import Stage
from app.models.content_block import ContentBlock
from app.models.progress import Progress
from app.models.onboarding_flow import OnboardingFlow
from app.models.company import Company


class NewHireService:
    """Service for managing new hires and their progress"""
    
    @staticmethod
    def create_new_hire(db: Session, company_id: str, new_hire_data: dict) -> Dict[str, Any]:
        """Create a new hire"""
        try:
            # Generate unique session token
            session_token = secrets.token_urlsafe(32)
            
            # Set token expiration (7 days from now)
            token_expires_at = datetime.utcnow() + timedelta(days=7)
            
            company_uuid = uuid.UUID(company_id)
            flow_uuid = uuid.UUID(new_hire_data["flow_id"])
            
            new_hire = NewHire(
                company_id=company_uuid,
                flow_id=flow_uuid,
                email=new_hire_data["email"],
                first_name=new_hire_data["first_name"],
                last_name=new_hire_data["last_name"],
                status="pending",
                session_token=session_token,
                session_token_expires_at=token_expires_at,
                invited_at=datetime.utcnow()
            )
            
            db.add(new_hire)
            db.commit()
            
            return {
                "success": True,
                "new_hire_id": str(new_hire.id),
                "session_token": session_token,
                "new_hire": new_hire
            }
            
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def send_invitation(db: Session, new_hire_id: str) -> Dict[str, Any]:
        """Send invitation email to new hire"""
        try:
            new_hire_uuid = uuid.UUID(new_hire_id)
            new_hire = db.query(NewHire).filter(NewHire.id == new_hire_uuid).first()
            
            if not new_hire:
                return {"success": False, "error": "New hire not found"}
            
            # TODO: Implement actual email sending
            # For now, just update the invited_at timestamp
            new_hire.invited_at = datetime.utcnow()
            db.commit()
            
            return {
                "success": True,
                "message": "Invitation sent successfully",
                "session_token": new_hire.session_token
            }
            
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def resend_invitation(db: Session, new_hire_id: str) -> Dict[str, Any]:
        """Resend invitation email to new hire"""
        try:
            new_hire_uuid = uuid.UUID(new_hire_id)
            new_hire = db.query(NewHire).filter(NewHire.id == new_hire_uuid).first()
            
            if not new_hire:
                return {"success": False, "error": "New hire not found"}

            # TODO: Send email to user with new session token
            # EmailService.send_token_renewal_email(
            #     to_email=new_hire.email,
            #     new_session_token=new_hire.session_token,
            #     expires_at=new_hire.session_token_expires_at,
            #     onboarding_url=f"https://yourdomain.com/onboarding/{new_hire.session_token}"
            # )
            
            # Update invited_at timestamp
            new_hire.invited_at = datetime.utcnow()
            db.commit()
            
            return {
                "success": True,
                "message": "Invitation resent successfully",
                "session_token": new_hire.session_token
            }
            
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_progress(db: Session, new_hire_id: str) -> Dict[str, Any]:
        """Get overall progress for a new hire"""
        try:
            new_hire_uuid = uuid.UUID(new_hire_id)
            new_hire = db.query(NewHire).filter(NewHire.id == new_hire_uuid).first()
            
            if not new_hire:
                return {"success": False, "error": "New hire not found"}
            
            # Get flow and stages
            flow = db.query(OnboardingFlow).filter(OnboardingFlow.id == new_hire.flow_id).first()
            stages = db.query(Stage).filter(Stage.flow_id == new_hire.flow_id).order_by(Stage.order).all()
            
            # Calculate progress
            total_stages = len(stages)
            completed_stages = 0
            
            stage_progress = []
            for stage in stages:
                is_complete = NewHireService.is_stage_complete(db, new_hire_id, str(stage.id))
                if is_complete:
                    completed_stages += 1
                
                stage_progress.append({
                    "stage_id": str(stage.id),
                    "stage_name": stage.name,
                    "is_complete": is_complete
                })
            
            progress_percentage = (completed_stages / total_stages * 100) if total_stages > 0 else 0
            
            return {
                "success": True,
                "progress": {
                    "new_hire_id": str(new_hire.id),
                    "flow_id": str(flow.id),
                    "flow_name": flow.name,
                    "total_stages": total_stages,
                    "completed_stages": completed_stages,
                    "progress_percentage": progress_percentage,
                    "status": new_hire.status,
                    "started_at": new_hire.started_at,
                    "completed_at": new_hire.completed_at,
                    "stage_progress": stage_progress
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_progress_by_stage(db: Session, new_hire_id: str, stage_id: str) -> Dict[str, Any]:
        """Get progress for a specific stage"""
        try:
            new_hire_uuid = uuid.UUID(new_hire_id)
            new_hire = db.query(NewHire).filter(NewHire.id == new_hire_uuid).first()
            
            if not new_hire:
                return {"success": False, "error": "New hire not found"}
            
            stage_uuid = uuid.UUID(stage_id)
            stage = db.query(Stage).filter(Stage.id == stage_uuid).first()
            
            if not stage:
                return {"success": False, "error": "Stage not found"}
            
            # Get content blocks for the stage
            content_blocks = db.query(ContentBlock).filter(
                ContentBlock.stage_id == stage_uuid
            ).order_by(ContentBlock.order_index).all()
            
            # Get progress for each content block
            content_block_progress = []
            for cb in content_blocks:
                progress = db.query(Progress).filter(
                    Progress.new_hire_id == new_hire_uuid,
                    Progress.content_block_id == cb.id
                ).first()
                
                content_block_progress.append({
                    "content_block_id": str(cb.id),
                    "type": cb.type,
                    "status": progress.status if progress else "pending",
                    "data": progress.data if progress else None,
                    "started_at": progress.started_at if progress else None,
                    "completed_at": progress.completed_at if progress else None
                })
            
            is_complete = NewHireService.is_stage_complete(db, new_hire_id, stage_id)
            
            return {
                "success": True,
                "stage_progress": {
                    "stage_id": str(stage.id),
                    "stage_name": stage.name,
                    "is_complete": is_complete,
                    "content_blocks": content_block_progress
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_progress_by_content_block(db: Session, new_hire_id: str, content_block_id: str) -> Dict[str, Any]:
        """Get progress for a specific content block"""
        try:
            new_hire_uuid = uuid.UUID(new_hire_id)
            new_hire = db.query(NewHire).filter(NewHire.id == new_hire_uuid).first()
            
            if not new_hire:
                return {"success": False, "error": "New hire not found"}
            
            content_block_uuid = uuid.UUID(content_block_id)
            content_block = db.query(ContentBlock).filter(ContentBlock.id == content_block_uuid).first()
            
            if not content_block:
                return {"success": False, "error": "Content block not found"}
            
            progress = db.query(Progress).filter(
                Progress.new_hire_id == new_hire_uuid,
                Progress.content_block_id == content_block_uuid
            ).first()
            
            return {
                "success": True,
                "content_block_progress": {
                    "content_block_id": str(content_block.id),
                    "type": content_block.type,
                    "status": progress.status if progress else "pending",
                    "data": progress.data if progress else None,
                    "started_at": progress.started_at if progress else None,
                    "completed_at": progress.completed_at if progress else None
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def is_stage_complete(db: Session, new_hire_id: str, stage_id: str) -> bool:
        """Check if a stage is complete for a new hire"""
        try:
            new_hire_uuid = uuid.UUID(new_hire_id)
            stage_uuid = uuid.UUID(stage_id)
            
            # Get all content blocks for the stage
            content_blocks = db.query(ContentBlock).filter(ContentBlock.stage_id == stage_uuid).all()
            
            if not content_blocks:
                return True  # Empty stage is considered complete
            
            # Check if all content blocks are completed
            for cb in content_blocks:
                progress = db.query(Progress).filter(
                    Progress.new_hire_id == new_hire_uuid,
                    Progress.content_block_id == cb.id
                ).first()
                
                if not progress or progress.status != "completed":
                    return False
            
            return True
            
        except Exception as e:
            return False
    
    @staticmethod
    def update_progress(
        db: Session,
        new_hire_id: str,
        stage_id: str,
        content_block_id: str,
        data: dict
    ) -> Dict[str, Any]:
        """Update progress for a content block"""
        try:
            new_hire_uuid = uuid.UUID(new_hire_id)
            stage_uuid = uuid.UUID(stage_id)
            content_block_uuid = uuid.UUID(content_block_id)
            
            new_hire = db.query(NewHire).filter(NewHire.id == new_hire_uuid).first()
            
            if not new_hire:
                return {"success": False, "error": "New hire not found"}
            
            # Create or update progress
            progress = db.query(Progress).filter(
                Progress.new_hire_id == new_hire_uuid,
                Progress.content_block_id == content_block_uuid
            ).first()
            
            if not progress:
                progress = Progress(
                    new_hire_id=new_hire_uuid,
                    stage_id=stage_uuid,
                    content_block_id=content_block_uuid,
                    status="completed",
                    data=data,
                    started_at=datetime.utcnow(),
                    completed_at=datetime.utcnow()
                )
                db.add(progress)
            else:
                progress.status = "completed"
                progress.data = data
                progress.completed_at = datetime.utcnow()
            
            db.commit()
            
            return {
                "success": True,
                "progress": progress
            }
            
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_new_hire_by_session_token(db: Session, session_token: str) -> Optional[NewHire]:
        """Get new hire by session token"""
        return db.query(NewHire).filter(NewHire.session_token == session_token).first()
    
    @staticmethod
    def get_new_hires_by_company(db: Session, company_id: str) -> List[NewHire]:
        """Get all new hires for a company"""
        company_uuid = uuid.UUID(company_id)
        return db.query(NewHire).filter(NewHire.company_id == company_uuid).all()
    
    @staticmethod
    def get_new_hires_by_flow(db: Session, flow_id: str) -> List[NewHire]:
        """Get all new hires for a specific flow"""
        flow_uuid = uuid.UUID(flow_id)
        return db.query(NewHire).filter(NewHire.flow_id == flow_uuid).all()