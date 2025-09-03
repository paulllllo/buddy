# content.py
"""
Content block schemas and discriminated union for create/update endpoints.
Config schemas and block classes are defined in content_block_config.py.
"""
from typing import Optional, List, Dict, Any, Union, Literal
from pydantic import BaseModel, Field, field_validator, root_validator, ValidationError
from datetime import datetime
import uuid
from .content_block_config import (
    HeaderBlock, DescriptionBlock, MediaBlock, SingleChoiceBlock, MultipleChoiceBlock, TextInputBlock, TextAreaBlock,
    FileUploadBlock, ExternalLinkBlock, ChecklistBlock, CautionBlock, ListBlock, DateBlock, TimePickerBlock, RatingScaleBlock, VisualAudioBlock,
    HeaderConfig, DescriptionConfig, MediaConfig, SingleChoiceConfig, MultipleChoiceConfig, TextInputConfig, TextAreaConfig,
    FileUploadConfig, ExternalLinkConfig, ChecklistConfig, CautionConfig, ListConfig, DateConfig, TimePickerConfig, RatingScaleConfig, VisualAudioConfig,
    HeaderBlockUpdate, DescriptionBlockUpdate, MediaBlockUpdate, SingleChoiceBlockUpdate, MultipleChoiceBlockUpdate, TextInputBlockUpdate, TextAreaBlockUpdate,
    FileUploadBlockUpdate, ExternalLinkBlockUpdate, ChecklistBlockUpdate, CautionBlockUpdate, ListBlockUpdate, DateBlockUpdate, TimePickerBlockUpdate, RatingScaleBlockUpdate, VisualAudioBlockUpdate
    )


class ContentTypeBase(BaseModel):
    name: str
    display_name: str
    description: Optional[str] = None
    category: Optional[str] = None
    default_config: Optional[Dict[str, Any]] = None


class ContentTypeCreate(ContentTypeBase):
    pass


class ContentTypeResponse(ContentTypeBase):
    id: str
    is_active: bool
    created_at: datetime
    
    @field_validator('id', mode='before')
    @classmethod
    def convert_uuid_to_string(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True


# --- Content Block Schemas ---

class ContentBlockBase(BaseModel):
    type: str
    config: Dict[str, Any]
    content: Dict[str, Any]
    order_index: int

class ContentBlockResponse(ContentBlockBase):
    id: str
    stage_id: str
    created_at: datetime
    updated_at: datetime
    
    @field_validator('id', 'stage_id', mode='before')
    @classmethod
    def convert_uuid_to_string(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True

# --- Discriminated Unions ---
class ContentBlockCreate(BaseModel):
    type: str = Field(..., description="Content type identifier")
    config: Dict[str, Any]
    content: Dict[str, Any]
    order_index: Optional[int] = None

    @root_validator(pre=True)
    @classmethod
    def validate_specific_type(cls, data: Any):
        if isinstance(data, dict):
            content_type = data.get('type')
            validators = {
                "header": HeaderBlock,
                "description": DescriptionBlock,
                "media": MediaBlock,
                "single_choice": SingleChoiceBlock,
                "multiple_choice": MultipleChoiceBlock,
                "text_input": TextInputBlock,
                "text_area": TextAreaBlock,
                "file_upload": FileUploadBlock,
                "external_link": ExternalLinkBlock,
                "checklist": ChecklistBlock,
                "caution": CautionBlock,
                "list": ListBlock,
                "date": DateBlock,
                "time_picker": TimePickerBlock,
                "rating_scale": RatingScaleBlock,
                "visual_audio": VisualAudioBlock
            }
            
            if not content_type:
                raise ValueError("Missing required field 'type'")
                
            if content_type not in validators:
                raise ValueError(f"Invalid content type: {content_type}")
            
            # Validate against specific schema
            try:
                validated = validators[content_type](**data)
                return validated.model_dump()
            except ValidationError as e:
                # Remap errors to base schema fields by removing content_type from loc
                errors = []
                for error in e.errors():
                    new_loc = []
                    for part in error["loc"]:
                        if part != content_type:  # Filter out content_type from location
                            new_loc.append(part)
                    error["loc"] = tuple(new_loc)
                    errors.append(error)
                raise ValidationError.from_exception_data(
                    title=cls.__name__,
                    line_errors=errors
                )
                
        return data

# --- Discriminated Union for Update ---
ContentBlockUpdate = Union[
    HeaderBlockUpdate,
    DescriptionBlockUpdate,
    MediaBlockUpdate,
    SingleChoiceBlockUpdate,
    MultipleChoiceBlockUpdate,
    TextInputBlockUpdate,
    TextAreaBlockUpdate,
    FileUploadBlockUpdate,
    ExternalLinkBlockUpdate,
    ChecklistBlockUpdate,
    CautionBlockUpdate,
    ListBlockUpdate,
    DateBlockUpdate,
    TimePickerBlockUpdate,
    RatingScaleBlockUpdate,
    VisualAudioBlockUpdate
]

class ContentBlockOrderItem(BaseModel):
    id: str = Field(description="Content block UUID")
    order_index: int = Field(description="New order position (1-based)", ge=1)

class ContentBlockReorder(BaseModel):
    content_blocks: List[ContentBlockOrderItem] = Field(
        description="List of content blocks with their new order positions",
        min_items=1,
        example=[
            {"id": "550e8400-e29b-41d4-a716-446655440000", "order_index": 1},
            {"id": "550e8400-e29b-41d4-a716-446655440001", "order_index": 2},
            {"id": "550e8400-e29b-41d4-a716-446655440002", "order_index": 3}
        ]
    )


class ContentValidationRequest(BaseModel):
    type: str
    config: Dict[str, Any]
    content: Dict[str, Any]


class ContentValidationResponse(BaseModel):
    valid: bool
    errors: List[str] = []
    content_type: Optional[str] = None


class StageTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str
    default_content: List[Dict[str, Any]]
    default_config: Dict[str, Any]
    is_public: bool = True


class StageTemplateCreate(StageTemplateBase):
    pass


class StageTemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    default_content: Optional[List[Dict[str, Any]]] = None
    default_config: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None


class StageTemplateResponse(StageTemplateBase):
    id: str
    created_at: datetime
    
    @field_validator('id', mode='before')
    @classmethod
    def convert_uuid_to_string(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True


class StageBase(BaseModel):
    name: str
    description: Optional[str] = None
    order: int
    type: Optional[str] = None
    status: str = "active"


class StageCreate(StageBase):
    pass


class StageUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    type: Optional[str] = None
    status: Optional[str] = None


class StageResponse(StageBase):
    id: str
    flow_id: str
    created_at: datetime
    content_blocks: List[ContentBlockResponse] = []
    
    @field_validator('id', 'flow_id', mode='before')
    @classmethod
    def convert_uuid_to_string(cls, v):
        if isinstance(v, uuid.UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True 