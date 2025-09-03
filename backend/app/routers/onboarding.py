from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.new_hire import NewHire
from app.models.stage import Stage
from app.models.content_block import ContentBlock
from app.models.progress import Progress
from app.models.onboarding_flow import OnboardingFlow
from app.auth.dependencies import get_current_new_hire
from app.services.onboarding_service import OnboardingSessionService
from app.schemas.onboarding import (
    OnboardingSession,
    StageCompletion,
    ContentBlockCompletion,
    ProgressOverview,
    FileUpload
)

router = APIRouter()


@router.get("/{session_token}", response_model=OnboardingSession)
async def get_onboarding_session(
    session_token: str,
    db: Session = Depends(get_db)
):
    """Get onboarding session details"""
    session_data = OnboardingSessionService.get_session_data(db, session_token)
    
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Onboarding session not found"
        )
    
    # Check if session data contains an error
    if "error" in session_data:
        if session_data["error"] == "session_token_expired":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=session_data
            )
        elif session_data["error"] == "access_denied":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=session_data
            )
    
    return session_data


@router.post("/{session_token}/start")
async def start_onboarding(
    session_token: str,
    db: Session = Depends(get_db)
):
    """Start the onboarding process"""
    result = OnboardingSessionService.start_onboarding(db, session_token)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return {"message": "Onboarding started successfully", "data": result["data"]}


@router.get("/{session_token}/progress", response_model=ProgressOverview)
async def get_progress_overview(
    session_token: str,
    db: Session = Depends(get_db)
):
    """Get overall progress for the onboarding session"""
    progress = OnboardingSessionService.get_progress_overview(db, session_token)
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Onboarding session not found"
        )
    
    return progress


@router.get("/{session_token}/current-stage")
async def get_current_stage(
    session_token: str,
    db: Session = Depends(get_db)
):
    """Get the current stage for the onboarding session"""
    current_stage = OnboardingSessionService.get_current_stage(db, session_token)
    
    if not current_stage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No current stage found"
        )
    
    return current_stage


@router.get("/{session_token}/stages/{stage_id}")
async def get_stage_with_content_blocks(
    session_token: str,
    stage_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific stage with all its content blocks and progress"""
    stage_data = OnboardingSessionService.get_stage_with_content_blocks(
        db, session_token, stage_id
    )
    
    if not stage_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stage not found"
        )
    
    return stage_data


@router.get("/{session_token}/stages/{stage_id}/status")
async def get_stage_status(
    session_token: str,
    stage_id: str,
    db: Session = Depends(get_db)
):
    """Get completion status for a specific stage"""
    status_data = OnboardingSessionService.get_stage_status(db, session_token, stage_id)
    
    if not status_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stage not found"
        )
    
    return status_data


@router.post("/{session_token}/stages/{stage_id}/content-blocks/{content_block_id}/complete")
async def complete_content_block(
    session_token: str,
    stage_id: str,
    content_block_id: str,
    completion_data: ContentBlockCompletion,
    db: Session = Depends(get_db)
):
    """Complete a content block"""
    result = OnboardingSessionService.complete_content_block(
        db, session_token, stage_id, content_block_id, completion_data.model_dump()
    )
    
    if not result["success"]:
        return result
        # raise HTTPException(
        #     status_code=status.HTTP_400_BAD_REQUEST,
        #     detail=result["error"]
        # )
    
    return {"message": "Content block completed successfully", "data": result["data"]}


@router.post("/{session_token}/stages/{stage_id}/complete")
async def complete_stage(
    session_token: str,
    stage_id: str,
    db: Session = Depends(get_db)
):
    """Complete a stage"""
    result = OnboardingSessionService.complete_stage(db, session_token, stage_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return {"message": "Stage completed successfully", "data": result["data"]}


@router.post("/{session_token}/uploads")
async def upload_file(
    session_token: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a file for the onboarding session"""
    result = OnboardingSessionService.upload_file(db, session_token, file)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return {"message": "File uploaded successfully", "data": result["data"]}


@router.post("/{session_token}/complete")
async def complete_onboarding(
    session_token: str,
    db: Session = Depends(get_db)
):
    """Complete the entire onboarding process"""
    result = OnboardingSessionService.complete_onboarding(db, session_token)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return {"message": "Onboarding completed successfully", "data": result["data"]} 