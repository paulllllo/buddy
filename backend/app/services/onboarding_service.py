from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
from app.models.new_hire import NewHire
from app.models.stage import Stage
from app.models.content_block import ContentBlock
from app.models.progress import Progress
from app.models.onboarding_flow import OnboardingFlow
from app.models.company import Company
from app.services.content_service import ContentService
from app.storage.factory import get_storage
import secrets


class OnboardingSessionService:
    """Service for managing onboarding sessions and progress tracking"""
    
    @staticmethod
    def get_session_data(db: Session, session_token: str) -> Optional[Dict[str, Any]]:
        """Get complete onboarding session data"""
        new_hire = db.query(NewHire).filter(NewHire.session_token == session_token).first()
        
        if not new_hire:
            return None
        
        # Check if token is expired
        if new_hire.is_session_token_expired():
            return {
                "error": "session_token_expired",
                "message": "Your onboarding session has expired. Please contact your administrator for a new invitation.",
                "expired_at": new_hire.session_token_expires_at.isoformat() if new_hire.session_token_expires_at else None
            }
        
        # Check if new hire can access onboarding
        if not new_hire.can_access_onboarding():
            return {
                "error": "access_denied",
                "message": "You cannot access onboarding at this time. Please contact your administrator.",
                "status": new_hire.status
            }
        
        # Get flow and company data
        flow = db.query(OnboardingFlow).filter(OnboardingFlow.id == new_hire.flow_id).first()
        company = db.query(Company).filter(Company.id == new_hire.company_id).first()
        
        if not flow or not company:
            return None
        
        # Get all stages with content blocks and progress
        stages = db.query(Stage).filter(Stage.flow_id == flow.id).order_by(Stage.order).all()
        
        stage_progress = []
        for stage in stages:
            content_blocks = ContentService.get_content_blocks_by_stage(db, str(stage.id))
            
            # Get progress for each content block
            content_block_progress = []
            for cb in content_blocks:
                progress = db.query(Progress).filter(
                    Progress.new_hire_id == new_hire.id,
                    Progress.content_block_id == cb.id
                ).first()
                
                content_block_progress.append({
                    "id": str(cb.id),
                    "type": cb.type,
                    "config": cb.config,
                    "content": cb.content,
                    "order_index": cb.order_index,
                    "status": progress.status if progress else "pending",
                    "data": progress.data if progress else None,
                    "started_at": progress.started_at if progress else None,
                    "completed_at": progress.completed_at if progress else None
                })
            
            # Check if stage is complete
            is_complete = OnboardingSessionService.is_stage_complete(db, session_token, str(stage.id))
            
            stage_progress.append({
                "id": str(stage.id),
                "name": stage.name,
                "description": stage.description,
                "order": stage.order,
                "type": stage.type,
                "status": stage.status,
                "content_blocks": content_block_progress,
                "is_complete": is_complete,
                "started_at": None,  # TODO: Add stage-level progress tracking
                "completed_at": None
            })
        
        return {
            "session_token": session_token,
            "new_hire_id": str(new_hire.id),
            "flow_id": str(flow.id),
            "flow_name": flow.name,
            "company_name": company.name,
            "company_logo_url": company.logo_url,
            "new_hire_name": f"{new_hire.first_name} {new_hire.last_name}",
            "new_hire_email": new_hire.email,
            "status": new_hire.status,
            "current_stage_id": OnboardingSessionService.get_current_stage_id(db, session_token),
            "started_at": new_hire.started_at,
            "completed_at": new_hire.completed_at,
            "stages": stage_progress
        }
    
    @staticmethod
    def start_onboarding(db: Session, session_token: str) -> Dict[str, Any]:
        """Start the onboarding process"""
        new_hire = db.query(NewHire).filter(NewHire.session_token == session_token).first()
        
        if not new_hire:
            return {"success": False, "error": "Onboarding session not found"}
        
        if new_hire.status == "completed":
            return {"success": False, "error": "Onboarding already completed"}
        
        # Update status and started_at
        new_hire.status = "started"
        new_hire.started_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "success": True,
            "data": {
                "status": "started",
                "started_at": new_hire.started_at
            }
        }
    
    @staticmethod
    def get_progress_overview(db: Session, session_token: str) -> Optional[Dict[str, Any]]:
        """Get overall progress for the onboarding session"""
        new_hire = db.query(NewHire).filter(NewHire.session_token == session_token).first()
        
        if not new_hire:
            return None
        
        # Get flow and stages
        flow = db.query(OnboardingFlow).filter(OnboardingFlow.id == new_hire.flow_id).first()
        stages = db.query(Stage).filter(Stage.flow_id == flow.id).order_by(Stage.order).all()
        
        # Count completed stages
        completed_stages = 0
        for stage in stages:
            if OnboardingSessionService.is_stage_complete(db, session_token, str(stage.id)):
                completed_stages += 1
        
        # Calculate progress percentage
        total_stages = len(stages)
        progress_percentage = (completed_stages / total_stages * 100) if total_stages > 0 else 0
        
        # Get current stage
        current_stage_id = OnboardingSessionService.get_current_stage_id(db, session_token)
        current_stage_name = None
        if current_stage_id:
            current_stage = db.query(Stage).filter(Stage.id == current_stage_id).first()
            current_stage_name = current_stage.name if current_stage else None
        
        return {
            "session_token": session_token,
            "new_hire_id": str(new_hire.id),
            "flow_id": str(flow.id),
            "total_stages": total_stages,
            "completed_stages": completed_stages,
            "current_stage_id": current_stage_id,
            "current_stage_name": current_stage_name,
            "overall_progress_percentage": progress_percentage,
            "started_at": new_hire.started_at,
            "estimated_completion_time": None  # TODO: Calculate based on remaining stages
        }
    
    @staticmethod
    def get_current_stage(db: Session, session_token: str) -> Optional[Dict[str, Any]]:
        """Get the current stage for the onboarding session"""
        current_stage_id = OnboardingSessionService.get_current_stage_id(db, session_token)
        
        if not current_stage_id:
            return None
        
        stage = db.query(Stage).filter(Stage.id == current_stage_id).first()
        
        if not stage:
            return None
        
        return {
            "id": str(stage.id),
            "name": stage.name,
            "description": stage.description,
            "order": stage.order,
            "type": stage.type
        }
    
    @staticmethod
    def get_stage_with_content_blocks(db: Session, session_token: str, stage_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific stage with all its content blocks and progress"""
        new_hire = db.query(NewHire).filter(NewHire.session_token == session_token).first()
        
        if not new_hire:
            return None
        
        stage = db.query(Stage).filter(Stage.id == stage_id).first()
        
        if not stage:
            return None
        
        # Get content blocks with progress
        content_blocks = ContentService.get_content_blocks_by_stage(db, stage_id)
        
        content_block_progress = []
        for cb in content_blocks:
            progress = db.query(Progress).filter(
                Progress.new_hire_id == new_hire.id,
                Progress.content_block_id == cb.id
            ).first()
            
            content_block_progress.append({
                "id": str(cb.id),
                "type": cb.type,
                "config": cb.config,
                "content": cb.content,
                "order_index": cb.order_index,
                "status": progress.status if progress else "pending",
                "data": progress.data if progress else None,
                "started_at": progress.started_at if progress else None,
                "completed_at": progress.completed_at if progress else None
            })
        
        return {
            "id": str(stage.id),
            "name": stage.name,
            "description": stage.description,
            "order": stage.order,
            "type": stage.type,
            "content_blocks": content_block_progress
        }
    
    @staticmethod
    def is_stage_complete(db: Session, session_token: str, stage_id: str) -> bool:
        """Check if a stage is complete"""
        new_hire = db.query(NewHire).filter(NewHire.session_token == session_token).first()
        
        if not new_hire:
            return False
        
        # Get all content blocks for the stage
        content_blocks = ContentService.get_content_blocks_by_stage(db, stage_id)
        
        if not content_blocks:
            return True  # Empty stage is considered complete
        
        # Check if all content blocks are completed
        for cb in content_blocks:
            progress = db.query(Progress).filter(
                Progress.new_hire_id == new_hire.id,
                Progress.content_block_id == cb.id
            ).first()
            
            if not progress or progress.status != "completed":
                return False
        
        return True
    
    @staticmethod
    def complete_content_block(
        db: Session,
        session_token: str,
        stage_id: str,
        content_block_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Complete a specific content block with collected data"""
        new_hire = db.query(NewHire).filter(NewHire.session_token == session_token).first()
        
        if not new_hire:
            return {"success": False, "error": "Onboarding session not found"}
        
        # Check if content block exists
        content_block = ContentService.get_content_block(db, content_block_id)
        if not content_block:
            return {"success": False, "error": "Content block not found"}
        
        # Validate user-submitted input against this block's type and config (not admin config validation)
        validation = OnboardingSessionService.validate_user_input_data(
            content_block=content_block,
            data=data or {}
        )
        if not validation.get("valid", False):
            return {
                "success": False,
                "error": "Validation failed",
                "details": validation.get("errors", [])
            }
        
        # Create or update progress
        progress = db.query(Progress).filter(
            Progress.new_hire_id == new_hire.id,
            Progress.content_block_id == content_block.id
        ).first()
        
        if not progress:
            progress = Progress(
                new_hire_id=new_hire.id,
                stage_id=uuid.UUID(stage_id) if isinstance(stage_id, str) else stage_id,
                content_block_id=content_block.id,
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
            "data": {
                "content_block_id": str(content_block.id),
                "status": "completed",
                "data": data
            }
        }
    
    @staticmethod
    def complete_stage(db: Session, session_token: str, stage_id: str) -> Dict[str, Any]:
        """Mark a stage as complete"""
        # Check if stage is actually complete
        if not OnboardingSessionService.is_stage_complete(db, session_token, stage_id):
            return {"success": False, "error": "Stage is not complete. All content blocks must be finished."}
        
        # Stage is already complete based on content block completion
        return {"success": True}
    
    @staticmethod
    def upload_file(db: Session, session_token: str, file) -> Dict[str, Any]:
        """Upload a file for the onboarding session"""
        new_hire = db.query(NewHire).filter(NewHire.session_token == session_token).first()
        
        if not new_hire:
            return {"success": False, "error": "Onboarding session not found"}
        
        try:
            # Get storage service
            storage = get_storage()
            
            # Generate file path
            file_path = f"onboarding/{new_hire.id}/{file.filename}"
            
            # Upload file
            file_url = storage.upload_file(file, file_path)
            
            return {
                "success": True,
                "file_url": file_url
            }
        except Exception as e:
            return {"success": False, "error": f"File upload failed: {str(e)}"}
    
    @staticmethod
    def complete_onboarding(db: Session, session_token: str) -> Dict[str, Any]:
        """Complete the entire onboarding process"""
        new_hire = db.query(NewHire).filter(NewHire.session_token == session_token).first()
        
        if not new_hire:
            return {"success": False, "error": "Onboarding session not found"}
        
        if new_hire.status == "completed":
            return {"success": False, "error": "Onboarding already completed"}
        
        # Check if all stages are complete
        flow = db.query(OnboardingFlow).filter(OnboardingFlow.id == new_hire.flow_id).first()
        stages = db.query(Stage).filter(Stage.flow_id == flow.id).order_by(Stage.order).all()
        
        for stage in stages:
            if not OnboardingSessionService.is_stage_complete(db, session_token, str(stage.id)):
                return {"success": False, "error": "Cannot complete onboarding. All stages must be finished."}
        
        # Mark onboarding as complete
        new_hire.status = "completed"
        new_hire.completed_at = datetime.utcnow()
        
        db.commit()
        
        return {"success": True}
    
    @staticmethod
    def get_current_stage_id(db: Session, session_token: str) -> Optional[str]:
        """Get the ID of the current stage (first incomplete stage).
        Returns None when all stages are complete.
        """
        new_hire = db.query(NewHire).filter(NewHire.session_token == session_token).first()
        
        if not new_hire:
            return None
        
        # Get all stages in order
        stages = db.query(Stage).filter(Stage.flow_id == new_hire.flow_id).order_by(Stage.order).all()
        
        # Find first incomplete stage
        for stage in stages:
            if not OnboardingSessionService.is_stage_complete(db, session_token, str(stage.id)):
                return str(stage.id)
        
        # All stages are complete
        return None

    @staticmethod
    def renew_session_token(db: Session, session_token: str) -> Dict[str, Any]:
        """Renew an expired session token"""
        new_hire = db.query(NewHire).filter(NewHire.session_token == session_token).first()
        
        if not new_hire:
            return {"success": False, "error": "Session not found"}
        
        # Only allow renewal if token is expired
        if not new_hire.is_session_token_expired():
            return {"success": False, "error": "Token is not expired"}
        
        # Generate new session token
        new_session_token = secrets.token_urlsafe(32)
        new_expires_at = datetime.utcnow() + timedelta(days=7)  # 7 days expiration
        
        # Update new hire with new token
        new_hire.session_token = new_session_token
        new_hire.session_token_expires_at = new_expires_at
        new_hire.updated_at = datetime.utcnow()
        
        db.commit()
        
        # TODO: Send email to user with new session token
        # EmailService.send_token_renewal_email(
        #     to_email=new_hire.email,
        #     new_session_token=new_session_token,
        #     expires_at=new_expires_at,
        #     onboarding_url=f"https://yourdomain.com/onboarding/{new_session_token}"
        # )
        
        return {
            "success": True,
            "new_session_token": new_session_token,
            "expires_at": new_expires_at.isoformat(),
            "message": "Session token renewed successfully"
        }
    
    @staticmethod
    def validate_session_token(db: Session, session_token: str) -> Dict[str, Any]:
        """Validate session token and return status"""
        new_hire = db.query(NewHire).filter(NewHire.session_token == session_token).first()
        
        if not new_hire:
            return {"valid": False, "error": "session_not_found"}
        
        if new_hire.is_session_token_expired():
            return {
                "valid": False, 
                "error": "session_token_expired",
                "expired_at": new_hire.session_token_expires_at.isoformat() if new_hire.session_token_expires_at else None
            }
        
        if not new_hire.can_access_onboarding():
            return {"valid": False, "error": "access_denied", "status": new_hire.status}
        
        return {
            "valid": True,
            "new_hire_id": str(new_hire.id),
            "status": new_hire.status,
            "expires_at": new_hire.session_token_expires_at.isoformat() if new_hire.session_token_expires_at else None
        }

    @staticmethod
    def validate_user_input_data(*, content_block: ContentBlock, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate new-hire submitted data for a given content block.
        This is distinct from ContentService.validate_content_block which validates admin config.
        Returns: {"valid": bool, "errors": [..]}
        """
        errors: List[str] = []
        ctype = (content_block.type or "").strip()
        config = content_block.config or {}
        content = content_block.content or {}
        
        # The incoming data is wrapped in a 'data' key.
        user_input = data.get("data", {}) if isinstance(data, dict) else {}

        # Helpers
        def is_required() -> bool:
            return bool(config.get("required", False))

        def rules() -> List[Dict[str, Any]]:
            return ((config.get("validation") or {}).get("rules")) or []

        def rule_value(name: str, default=None):
            for r in rules():
                if r.get("type") == name:
                    return r.get("value")
            return default

        def option_ids() -> List[str]:
            ids: List[str] = []
            for o in content.get("options") or []:
                if isinstance(o, dict):
                    oid = o.get("id") or o.get("value")
                    if oid is not None:
                        ids.append(str(oid))
                else:
                    ids.append(str(o))
            return ids

        # Display-only types: automatically approve since they don't collect input
        display_only = {"header", "description", "media", "external_link", "list", "caution"}
        if ctype in display_only:
            return {"valid": True, "errors": []}
        
        # print(f"Validating user input for content block type '{ctype}' with data: {user_input}")

        # Input-capable types
        if ctype == "single_choice":
            answer = (user_input or {}).get("answer")
            if is_required() and (answer is None or str(answer) == ""):
                # print('Inside answer missing', answer)
                errors.append("answer is required")
            if answer is not None:
                if str(answer) not in option_ids():
                    # print('Inside answer missing', answer, option_ids())
                    errors.append("Selected answer is not in options")

        elif ctype == "multiple_choice":
            answers = (user_input or {}).get("answers")
            if is_required() and (answers is None or not isinstance(answers, list) or len(answers) == 0):
                errors.append("answers are required")
            if answers is not None:
                if not isinstance(answers, list):
                    errors.append("answers must be a list")
                else:
                    valid_ids = set(option_ids())
                    for a in answers:
                        if str(a) not in valid_ids:
                            errors.append(f"Selected answer '{a}' is not in options")
                    min_sel = rule_value("min_selections")
                    max_sel = rule_value("max_selections")
                    if isinstance(min_sel, int) and len(answers) < min_sel:
                        errors.append(f"At least {min_sel} selections required")
                    if isinstance(max_sel, int) and len(answers) > max_sel:
                        errors.append(f"At most {max_sel} selections allowed")

        elif ctype == "text_input":
            value = (user_input or {}).get("value")
            if is_required() and (value is None or str(value) == ""):
                errors.append("value is required")
            if value is not None:
                if not isinstance(value, str):
                    errors.append("value must be a string")
                else:
                    min_len = rule_value("min_length")
                    max_len = rule_value("max_length")
                    pattern = rule_value("pattern")
                    if isinstance(min_len, int) and len(value) < min_len:
                        errors.append(f"value must be at least {min_len} characters")
                    if isinstance(max_len, int) and len(value) > max_len:
                        errors.append(f"value must be at most {max_len} characters")
                    if isinstance(pattern, str):
                        import re
                        if re.fullmatch(pattern, value) is None:
                            errors.append("value does not match required pattern")

        elif ctype == "text_area":
            value = (user_input or {}).get("value")
            if is_required() and (value is None or str(value) == ""):
                errors.append("value is required")
            if value is not None:
                if not isinstance(value, str):
                    errors.append("value must be a string")
                else:
                    min_len = rule_value("min_length")
                    max_len = rule_value("max_length")
                    if isinstance(min_len, int) and len(value) < min_len:
                        errors.append(f"value must be at least {min_len} characters")
                    if isinstance(max_len, int) and len(value) > max_len:
                        errors.append(f"value must be at most {max_len} characters")

        elif ctype == "file_upload":
            files = (user_input or {}).get("files")
            if is_required() and (files is None or not isinstance(files, list) or len(files) == 0):
                errors.append("files are required")
            if files is not None:
                if not isinstance(files, list):
                    errors.append("files must be a list")
                else:
                    allowed_types = rule_value("file_type") or []
                    max_size = rule_value("file_size")
                    max_files = rule_value("max_files")
                    if isinstance(max_files, int) and len(files) > max_files:
                        errors.append(f"At most {max_files} files allowed")
                    for f in files:
                        if not isinstance(f, dict):
                            errors.append("each file must be an object with file_type and file_size")
                            continue
                        ftype = f.get("file_type")
                        fsize = f.get("file_size")
                        if allowed_types and ftype not in allowed_types:
                            errors.append(f"file_type '{ftype}' not allowed")
                        if isinstance(max_size, int) and isinstance(fsize, int) and fsize > max_size:
                            errors.append(f"file_size exceeds limit {max_size}")

        elif ctype == "checklist":
            checked = (user_input or {}).get("checked_items")
            if is_required() and (checked is None or not isinstance(checked, list) or len(checked) == 0):
                errors.append("checked_items are required")
            if checked is not None:
                if not isinstance(checked, list):
                    errors.append("checked_items must be a list")
                else:
                    valid_ids = set([str(i.get("id")) for i in (content.get("items") or []) if isinstance(i, dict) and i.get("id") is not None])
                    for cid in checked:
                        if str(cid) not in valid_ids:
                            errors.append(f"checked item '{cid}' is not in items")
                    min_sel = rule_value("min_selections")
                    if isinstance(min_sel, int) and len(checked) < min_sel:
                        errors.append(f"At least {min_sel} items must be checked")

        elif ctype == "date":
            date_val = (user_input or {}).get("date")
            if is_required() and (date_val is None or str(date_val) == ""):
                errors.append("date is required")
            if date_val is not None:
                try:
                    from datetime import date as _date, datetime as _dt, timedelta as _td
                    parsed = _dt.fromisoformat(str(date_val)).date()
                    today = _date.today()
                    def to_date(marker):
                        if not marker:
                            return None
                        if marker == "today":
                            return today
                        if isinstance(marker, str) and marker.startswith("+"):
                            import re
                            m = re.match(r"\+(\d+)(day|days|month|months|year|years)", marker)
                            if m:
                                qty = int(m.group(1)); unit = m.group(2)
                                if "day" in unit:
                                    return today + _td(days=qty)
                                if "month" in unit:
                                    return today + _td(days=qty*30)
                                if "year" in unit:
                                    return today + _td(days=qty*365)
                        try:
                            return _dt.fromisoformat(marker).date()
                        except Exception:
                            return None
                    min_d = to_date(rule_value("min_date"))
                    max_d = to_date(rule_value("max_date"))
                    if min_d and parsed < min_d:
                        errors.append("date is earlier than allowed minimum")
                    if max_d and parsed > max_d:
                        errors.append("date is later than allowed maximum")
                except Exception:
                    errors.append("date must be an ISO date string")

        elif ctype == "time_picker":
            time_val = (user_input or {}).get("time")
            if is_required() and (time_val is None or str(time_val) == ""):
                errors.append("time is required")
            if time_val is not None:
                try:
                    hh, mm, *_ = str(time_val).split(":")
                    hh = int(hh); mm = int(mm)
                    if not (0 <= hh <= 23 and 0 <= mm <= 59):
                        errors.append("time must be in HH:MM 24h format")
                    def minutes(tstr):
                        if not tstr or ":" not in tstr:
                            return None
                        h, m = tstr.split(":")[0:2]
                        return int(h) * 60 + int(m)
                    val_m = hh*60 + mm
                    min_m = minutes(rule_value("min_time"))
                    max_m = minutes(rule_value("max_time"))
                    if isinstance(min_m, int) and val_m < min_m:
                        errors.append("time is earlier than allowed minimum")
                    if isinstance(max_m, int) and val_m > max_m:
                        errors.append("time is later than allowed maximum")
                except Exception:
                    errors.append("time must be in HH:MM format")

        elif ctype == "rating_scale":
            rating = (user_input or {}).get("rating")
            if is_required() and (rating is None or str(rating) == ""):
                errors.append("rating is required")
            if rating is not None:
                try:
                    rating_val = int(rating)
                except Exception:
                    errors.append("rating must be an integer")
                else:
                    min_v = rule_value("min_value")
                    max_v = rule_value("max_value")
                    if isinstance(min_v, int) and rating_val < min_v:
                        errors.append(f"rating must be at least {min_v}")
                    if isinstance(max_v, int) and rating_val > max_v:
                        errors.append(f"rating must be at most {max_v}")

        elif ctype == "visual_audio":
            response = (user_input or {}).get("response")
            recording = (user_input or {}).get("recording")
            if is_required() and not (response or recording):
                errors.append("response or recording is required")
            if recording is not None:
                if not isinstance(recording, dict):
                    errors.append("recording must be an object with file_type and file_size")
                else:
                    allowed_types = rule_value("file_type") or []
                    max_size = rule_value("file_size")
                    rtype = recording.get("file_type")
                    rsize = recording.get("file_size")
                    if allowed_types and rtype not in allowed_types:
                        errors.append(f"recording file_type '{rtype}' not allowed")
                    if isinstance(max_size, int) and isinstance(rsize, int) and rsize > max_size:
                        errors.append(f"recording file_size exceeds limit {max_size}")

        else:
            errors.append(f"Unsupported content type '{ctype}' for user input validation")

        return {"valid": len(errors) == 0, "errors": errors}