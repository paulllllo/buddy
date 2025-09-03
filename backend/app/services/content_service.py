from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import uuid
from app.models.content_block import ContentBlock
from app.models.stage import Stage
from app.models.content_type import ContentType
from app.services.content_type_service import ContentTypeService


class ContentService:
    """Service for managing content blocks"""
    
    @staticmethod
    def create_content_block(
        db: Session,
        stage_id: str,
        content_type_name: str,
        config: Dict[str, Any],
        content: Dict[str, Any],
        order_index: Optional[int] = None
    ) -> ContentBlock:
        """Create a new content block"""
        # Verify content type exists
        content_type = ContentTypeService.get_content_type_by_name(db, content_type_name)
        if not content_type:
            raise ValueError(f"Content type '{content_type_name}' not found")
        
        stage_uuid = uuid.UUID(stage_id)
        
        # Get next order index if not provided
        if order_index is None:
            max_order = db.query(ContentBlock).filter(
                ContentBlock.stage_id == stage_uuid
            ).with_entities(
                db.func.max(ContentBlock.order_index)
            ).scalar() or 0
            order_index = max_order + 1
        
        if hasattr(config, 'dict'):
            config = config.dict()
        if hasattr(content, 'dict'):
            content = content.dict()
        
        content_block = ContentBlock(
            stage_id=stage_uuid,
            type=content_type_name,
            config=config,
            content=content,
            order_index=order_index
        )
        
        db.add(content_block)
        db.commit()
        db.refresh(content_block)
        return content_block
    
    @staticmethod
    def get_content_blocks_by_stage(db: Session, stage_id: str) -> List[ContentBlock]:
        """Get all content blocks for a stage, ordered by order_index"""
        stage_uuid = uuid.UUID(stage_id)
        return db.query(ContentBlock).filter(
            ContentBlock.stage_id == stage_uuid
        ).order_by(ContentBlock.order_index).all()
    
    @staticmethod
    def get_content_block(db: Session, content_block_id: str) -> Optional[ContentBlock]:
        """Get a specific content block"""
        content_block_uuid = uuid.UUID(content_block_id)
        return db.query(ContentBlock).filter(ContentBlock.id == content_block_uuid).first()
    
    @staticmethod
    def update_content_block(
        db: Session,
        content_block_id: str,
        config: Optional[Dict[str, Any]] = None,
        content: Optional[Dict[str, Any]] = None
    ) -> Optional[ContentBlock]:
        """Update a content block"""
        content_block = ContentService.get_content_block(db, content_block_id)
        if not content_block:
            return None
        
        def _deep_merge(original: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
            # Recursively merge nested dictionaries; arrays and scalars are replaced
            result = dict(original or {})
            for key, value in (updates or {}).items():
                if (
                    key in result
                    and isinstance(result[key], dict)
                    and isinstance(value, dict)
                ):
                    result[key] = _deep_merge(result[key], value)
                else:
                    result[key] = value
            return result

        # Merge incoming partial config/content into existing persisted values
        if config is not None:
            merged_config = _deep_merge(content_block.config or {}, config)
            content_block.config = merged_config
        if content is not None:
            merged_content = _deep_merge(content_block.content or {}, content)
            content_block.content = merged_content

        # Validate merged result against content type rules before saving
        if config is not None or content is not None:
            validation = ContentService.validate_content_block(
                db=db,
                content_type_name=content_block.type,
                config=content_block.config or {},
                content=content_block.content or {},
            )
            if not validation.get("valid", True):
                # Revert changes to avoid leaving invalid state in session
                db.rollback()
                raise ValueError(
                    "; ".join(validation.get("errors", ["Invalid content block configuration"]))
                )
        
        db.commit()
        db.refresh(content_block)
        return content_block
    
    @staticmethod
    def delete_content_block(db: Session, content_block_id: str) -> bool:
        """Delete a content block"""
        content_block = ContentService.get_content_block(db, content_block_id)
        if not content_block:
            return False
        
        db.delete(content_block)
        db.commit()
        return True
    
    @staticmethod
    def reorder_content_blocks(
        db: Session,
        stage_id: str,
        content_block_orders: List[Dict[str, Any]]
    ) -> List[ContentBlock]:
        """Reorder content blocks within a stage"""
        # content_block_orders should be: [{"id": "uuid", "order_index": 1}, ...]
        stage_uuid = uuid.UUID(stage_id)
        
        for item in content_block_orders:
            # Handle both dict and Pydantic model
            if hasattr(item, 'id') and hasattr(item, 'order_index'):
                # Pydantic model (ContentBlockOrderItem)
                block_id = item.id
                order_index = item.order_index
            else:
                # Dict format
                block_id = item["id"]
                order_index = item["order_index"]
            
            # Convert string ID to UUID for database query
            block_uuid = uuid.UUID(block_id)
            content_block = db.query(ContentBlock).filter(
                ContentBlock.id == block_uuid,
                ContentBlock.stage_id == stage_uuid
            ).first()
            
            if content_block:
                content_block.order_index = order_index
        
        db.commit()
        
        # Return updated content blocks
        return ContentService.get_content_blocks_by_stage(db, stage_id)
    
    @staticmethod
    def validate_content_block(
        db: Session,
        content_type_name: str,
        config: Dict[str, Any],
        content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate content block configuration and content"""
        # Get content type
        content_type = ContentTypeService.get_content_type_by_name(db, content_type_name)
        if not content_type:
            return {"valid": False, "error": f"Content type '{content_type_name}' not found"}
        
        # Basic validation based on content type
        validation_result = {"valid": True, "errors": []}
        
        # Validate required fields in content based on content type
        if content_type_name == "header":
            if "title" not in content or not content["title"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Header must have a title")
        
        elif content_type_name == "description":
            if "text" not in content or not content["text"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Description must have text content")
        
        elif content_type_name == "media":
            if "file_url" not in content or not content["file_url"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Media must have a file URL")
        
        elif content_type_name == "single_choice":
            if "question" not in content or not content["question"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Single choice must have a question")
            
            if "options" not in content or not content["options"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Single choice must have options")
            elif len(content["options"]) < 2:
                validation_result["valid"] = False
                validation_result["errors"].append("Single choice must have at least 2 options")
        
        elif content_type_name == "multiple_choice":
            if "question" not in content or not content["question"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Multiple choice must have a question")
            
            if "options" not in content or not content["options"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Multiple choice must have options")
            elif len(content["options"]) < 2:
                validation_result["valid"] = False
                validation_result["errors"].append("Multiple choice must have at least 2 options")
        
        elif content_type_name == "text_input":
            if "label" not in content or not content["label"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Text input must have a label")
        
        elif content_type_name == "text_area":
            if "label" not in content or not content["label"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Text area must have a label")
        
        elif content_type_name == "file_upload":
            if "label" not in content or not content["label"]:
                validation_result["valid"] = False
                validation_result["errors"].append("File upload must have a label")
        
        elif content_type_name == "external_link":
            if "url" not in content or not content["url"]:
                validation_result["valid"] = False
                validation_result["errors"].append("External link must have a URL")
            
            if "title" not in content or not content["title"]:
                validation_result["valid"] = False
                validation_result["errors"].append("External link must have a title")
        
        elif content_type_name == "checklist":
            if "title" not in content or not content["title"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Checklist must have a title")
            
            if "items" not in content or not content["items"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Checklist must have items")
            elif len(content["items"]) < 2:
                validation_result["valid"] = False
                validation_result["errors"].append("Checklist must have at least 2 items")
        
        elif content_type_name == "caution":
            if "message" not in content or not content["message"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Caution must have a message")
        
        elif content_type_name == "list":
            if "items" not in content or not content["items"]:
                validation_result["valid"] = False
                validation_result["errors"].append("List must have items")
            elif len(content["items"]) < 1:
                validation_result["valid"] = False
                validation_result["errors"].append("List must have at least one item")
        
        elif content_type_name == "date":
            if "label" not in content or not content["label"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Date picker must have a label")
        
        elif content_type_name == "time_picker":
            if "label" not in content or not content["label"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Time picker must have a label")
        
        elif content_type_name == "rating_scale":
            if "question" not in content or not content["question"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Rating scale must have a question")
        
        elif content_type_name == "visual_audio":
            if "title" not in content or not content["title"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Visual/audio content must have a title")
            
            if "prompt" not in content or not content["prompt"]:
                validation_result["valid"] = False
                validation_result["errors"].append("Visual/audio content must have a prompt")
        
        return validation_result 