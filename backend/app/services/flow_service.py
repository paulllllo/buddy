from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import uuid
from app.models.onboarding_flow import OnboardingFlow
from app.models.stage import Stage
from app.models.new_hire import NewHire
from app.models.progress import Progress
from app.models.content_block import ContentBlock
from app.services.stage_template_service import StageTemplateService


class FlowService:
    """Service for managing onboarding flows and related operations"""
    
    @staticmethod
    def create_flow(db: Session, company_id: str, flow_data: dict) -> Dict[str, Any]:
        """Create a new onboarding flow"""
        try:
            company_uuid = uuid.UUID(company_id)
            flow = OnboardingFlow(
                company_id=company_uuid,
                name=flow_data["name"],
                description=flow_data.get("description"),
                duration_days=flow_data.get("duration_days"),
                status=flow_data.get("status", "draft")
            )
            
            db.add(flow)
            db.commit()
            
            return {
                "success": True,
                "flow_id": str(flow.id),
                "flow": flow
            }
            
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def update_flow(db: Session, flow_id: str, data: dict) -> Dict[str, Any]:
        """Update an onboarding flow"""
        try:
            flow_uuid = uuid.UUID(flow_id)
            flow = db.query(OnboardingFlow).filter(OnboardingFlow.id == flow_uuid).first()
            
            if not flow:
                return {"success": False, "error": "Flow not found"}
            
            # Update fields
            for field, value in data.items():
                if hasattr(flow, field) and value is not None:
                    setattr(flow, field, value)
            
            flow.updated_at = datetime.utcnow()
            db.commit()
            
            return {"success": True, "flow": flow}
            
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def add_stage(db: Session, flow_id: str, stage_data: dict, template_id: str = None) -> Dict[str, Any]:
        """Add a new stage to an onboarding flow"""
        try:
            flow_uuid = uuid.UUID(flow_id)
            flow = db.query(OnboardingFlow).filter(OnboardingFlow.id == flow_uuid).first()
            
            if not flow:
                return {"success": False, "error": "Flow not found"}
            
            # Get the next order number
            max_order = db.query(Stage).filter(Stage.flow_id == flow_uuid).with_entities(
                func.max(Stage.order)
            ).scalar()
            next_order = (max_order or 0) + 1
            
            # Create stage
            stage = Stage(
                flow_id=flow_uuid,
                name=stage_data["name"],
                description=stage_data.get("description"),
                order=next_order,
                type=stage_data.get("type")
            )
            
            db.add(stage)
            db.flush()  # Get the stage ID
            
            # If template is provided, apply template content
            if template_id:
                template_result = FlowService._apply_stage_template(
                    db, str(stage.id), template_id
                )
                if not template_result["success"]:
                    print(f"Failed to apply template: {template_result['error']}")
                    # Continue even if template fails
                    pass
            
            db.commit()
            
            return {
                "success": True,
                "stage_id": str(stage.id),
                "stage": stage
            }
            
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def update_stage(db: Session, flow_id: str, stage_id: str, data: dict) -> Dict[str, Any]:
        """Update a stage in an onboarding flow"""
        try:
            flow_uuid = uuid.UUID(flow_id)
            stage_uuid = uuid.UUID(stage_id)
            stage = db.query(Stage).filter(
                Stage.id == stage_uuid,
                Stage.flow_id == flow_uuid
            ).first()
            
            if not stage:
                return {"success": False, "error": "Stage not found"}
            
            # Update fields
            for field, value in data.items():
                if hasattr(stage, field) and value is not None:
                    setattr(stage, field, value)
            
            db.commit()
            
            return {"success": True, "stage": stage}
            
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def reorder_stages(db: Session, flow_id: str, stage_order: List[str]) -> Dict[str, Any]:
        """Reorder stages in an onboarding flow"""
        try:
            flow_uuid = uuid.UUID(flow_id)
            # Update order for each stage
            for index, stage_id in enumerate(stage_order, 1):
                stage_uuid = uuid.UUID(stage_id)
                stage = db.query(Stage).filter(
                    Stage.id == stage_uuid,
                    Stage.flow_id == flow_uuid
                ).first()
                
                if stage:
                    stage.order = index
            
            db.commit()
            
            return {"success": True}
        
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_pipeline_data(db: Session, flow_id: str) -> Dict[str, Any]:
        """Get pipeline data showing new hires and their progress through stages"""
        try:
            flow_uuid = uuid.UUID(flow_id)
            flow = db.query(OnboardingFlow).filter(OnboardingFlow.id == flow_uuid).first()
            
            if not flow:
                return {"success": False, "error": "Flow not found"}
            
            # Get all stages for the flow
            stages = db.query(Stage).filter(Stage.flow_id == flow_uuid).order_by(Stage.order).all()
            
            # Get all new hires for the flow
            new_hires = db.query(NewHire).filter(NewHire.flow_id == flow_uuid).all()
            
            # Build pipeline data
            pipeline_data = {
                "flow": {
                    "id": str(flow.id),
                    "name": flow.name,
                    "status": flow.status
                },
                "stages": [],
                "new_hires": []
            }
            
            # Add stages
            for stage in stages:
                pipeline_data["stages"].append({
                    "id": str(stage.id),
                    "name": stage.name,
                    "order": stage.order,
                    "type": stage.type
                })
            
            # Add new hires with their current stage
            for new_hire in new_hires:
                # Find current stage (first incomplete stage)
                current_stage = FlowService._get_current_stage_for_new_hire(db, new_hire.id, stages)
                
                pipeline_data["new_hires"].append({
                    "id": str(new_hire.id),
                    "name": f"{new_hire.first_name} {new_hire.last_name}",
                    "email": new_hire.email,
                    "status": new_hire.status,
                    "current_stage_id": str(current_stage.id) if current_stage else None,
                    "current_stage_name": current_stage.name if current_stage else None,
                    "started_at": new_hire.started_at,
                    "completed_at": new_hire.completed_at
                })
            
            return {
                "success": True,
                "pipeline": pipeline_data
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_flow_stats(db: Session, flow_id: str) -> Dict[str, Any]:
        """Get statistics for a specific flow"""
        try:
            flow_uuid = uuid.UUID(flow_id)
            flow = db.query(OnboardingFlow).filter(OnboardingFlow.id == flow_uuid).first()
            
            if not flow:
                return {"success": False, "error": "Flow not found"}
            
            # Count new hires by status
            total_new_hires = db.query(NewHire).filter(NewHire.flow_id == flow_uuid).count()
            pending_new_hires = db.query(NewHire).filter(
                NewHire.flow_id == flow_uuid,
                NewHire.status == "pending"
            ).count()
            active_new_hires = db.query(NewHire).filter(
                NewHire.flow_id == flow_uuid,
                NewHire.status == "started"
            ).count()
            completed_new_hires = db.query(NewHire).filter(
                NewHire.flow_id == flow_uuid,
                NewHire.status == "completed"
            ).count()
            
            # Count stages
            total_stages = db.query(Stage).filter(Stage.flow_id == flow_uuid).count()
            
            return {
                "success": True,
                "stats": {
                    "flow": {
                        "id": str(flow.id),
                        "name": flow.name,
                        "status": flow.status,
                        "duration_days": flow.duration_days
                    },
                    "new_hires": {
                        "total": total_new_hires,
                        "pending": pending_new_hires,
                        "active": active_new_hires,
                        "completed": completed_new_hires
                    },
                    "stages": {
                        "total": total_stages
                    }
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def _apply_stage_template(db: Session, stage_id: str, template_id: str) -> Dict[str, Any]:
        """Apply a stage template to create content blocks"""
        try:
            template = StageTemplateService.get_template_by_id(db, template_id)
            
            if not template:
                return {"success": False, "error": "Template not found"}
            
            # Import content service here to avoid circular imports
            from app.services.content_service import ContentService
            
            # Apply template content blocks
            if template.default_content and template.default_config:
                for i, content_block in enumerate(template.default_content):
                    ContentService.create_content_block(
                        db=db,
                        stage_id=stage_id,
                        content_type_name=content_block.get("type"),
                        config=content_block.get("config", {}),
                        content=content_block.get("content", {}),
                        order_index=i + 1
                    )
            
            return {"success": True}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def _get_current_stage_for_new_hire(db: Session, new_hire_id: str, stages: List[Stage]) -> Optional[Stage]:
        """Get the current stage for a new hire (first incomplete stage)"""
        for stage in stages:
            # Check if stage is complete for this new hire
            content_blocks = db.query(ContentBlock).filter(ContentBlock.stage_id == stage.id).all()
            
            if not content_blocks:
                continue  # Empty stage, move to next
            
            # Check if all content blocks are completed
            all_completed = True
            for cb in content_blocks:
                progress = db.query(Progress).filter(
                    Progress.new_hire_id == new_hire_id,
                    Progress.content_block_id == cb.id
                ).first()
                
                if not progress or progress.status != "completed":
                    all_completed = False
                    break
            
            if not all_completed:
                return stage
        
        # All stages are complete, return the last stage
        return stages[-1] if stages else None 