"""
Config schemas and block classes for content blocks.
Imported by content.py for use in discriminated unions.
"""
from typing import Optional, List, Dict, Any, Literal, Union
from pydantic import BaseModel

# --- Shared ValidationConfig ---
class ValidationConfig(BaseModel):
    rules: List[Dict[str, Any]]
    messages: Dict[str, str]

# --- Config Schemas ---
class HeaderConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = False
    validation: ValidationConfig
    display: Dict[str, Any]
    style: Dict[str, Any]

class DescriptionConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = False
    validation: ValidationConfig
    display: Dict[str, Any]
    formatting: Dict[str, Any]

class MediaConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = False
    validation: ValidationConfig
    display: Dict[str, Any]
    media: Dict[str, Any]

class SingleChoiceConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = True
    validation: ValidationConfig
    display: Dict[str, Any]
    question: Dict[str, Any]

class MultipleChoiceConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = True
    validation: ValidationConfig
    display: Dict[str, Any]
    question: Dict[str, Any]

class TextInputConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = True
    validation: ValidationConfig
    display: Dict[str, Any]
    input: Dict[str, Any]

class TextAreaConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = True
    validation: ValidationConfig
    display: Dict[str, Any]
    input: Dict[str, Any]

class FileUploadConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = True
    validation: ValidationConfig
    display: Dict[str, Any]
    upload: Dict[str, Any]

class ExternalLinkConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = False
    validation: ValidationConfig
    display: Dict[str, Any]
    link: Dict[str, Any]

class ChecklistConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = True
    validation: ValidationConfig
    display: Dict[str, Any]
    checklist: Dict[str, Any]

class CautionConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = False
    validation: ValidationConfig
    display: Dict[str, Any]
    caution: Dict[str, Any]

class ListConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = False
    validation: ValidationConfig
    display: Dict[str, Any]
    list: Dict[str, Any]

class DateConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = True
    validation: ValidationConfig
    display: Dict[str, Any]
    date: Dict[str, Any]

class TimePickerConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = True
    validation: ValidationConfig
    display: Dict[str, Any]
    time: Dict[str, Any]

class RatingScaleConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = True
    validation: ValidationConfig
    display: Dict[str, Any]
    rating: Dict[str, Any]

class VisualAudioConfig(BaseModel):
    label: str
    description: Optional[str]
    required: bool = True
    validation: ValidationConfig
    display: Dict[str, Any]
    media: Dict[str, Any]

# --- Block Classes for Discriminated Union ---
class HeaderBlock(BaseModel):
    type: Literal["header"]
    config: HeaderConfig
    content: Dict[str, Any]
    order_index: int

class DescriptionBlock(BaseModel):
    type: Literal["description"]
    config: DescriptionConfig
    content: Dict[str, Any]
    order_index: int

class MediaBlock(BaseModel):
    type: Literal["media"]
    config: MediaConfig
    content: Dict[str, Any]
    order_index: int

class SingleChoiceBlock(BaseModel):
    type: Literal["single_choice"]
    config: SingleChoiceConfig
    content: Dict[str, Any]
    order_index: int

class MultipleChoiceBlock(BaseModel):
    type: Literal["multiple_choice"]
    config: MultipleChoiceConfig
    content: Dict[str, Any]
    order_index: int

class TextInputBlock(BaseModel):
    type: Literal["text_input"]
    config: TextInputConfig
    content: Dict[str, Any]
    order_index: int

class TextAreaBlock(BaseModel):
    type: Literal["text_area"]
    config: TextAreaConfig
    content: Dict[str, Any]
    order_index: int

class FileUploadBlock(BaseModel):
    type: Literal["file_upload"]
    config: FileUploadConfig
    content: Dict[str, Any]
    order_index: int

class ExternalLinkBlock(BaseModel):
    type: Literal["external_link"]
    config: ExternalLinkConfig
    content: Dict[str, Any]
    order_index: int

class ChecklistBlock(BaseModel):
    type: Literal["checklist"]
    config: ChecklistConfig
    content: Dict[str, Any]
    order_index: int

class CautionBlock(BaseModel):
    type: Literal["caution"]
    config: CautionConfig
    content: Dict[str, Any]
    order_index: int

class ListBlock(BaseModel):
    type: Literal["list"]
    config: ListConfig
    content: Dict[str, Any]
    order_index: int

class DateBlock(BaseModel):
    type: Literal["date"]
    config: DateConfig
    content: Dict[str, Any]
    order_index: int

class TimePickerBlock(BaseModel):
    type: Literal["time_picker"]
    config: TimePickerConfig
    content: Dict[str, Any]
    order_index: int

class RatingScaleBlock(BaseModel):
    type: Literal["rating_scale"]
    config: RatingScaleConfig
    content: Dict[str, Any]
    order_index: int

class VisualAudioBlock(BaseModel):
    type: Literal["visual_audio"]
    config: VisualAudioConfig
    content: Dict[str, Any]
    order_index: int

# --- Update Block Classes (All Fields Optional, for PATCH/PUT) ---
class HeaderBlockUpdate(BaseModel):
    type: Optional[Literal["header"]] = None
    # Accept partial config; backend will merge and validate
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class DescriptionBlockUpdate(BaseModel):
    type: Optional[Literal["description"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class MediaBlockUpdate(BaseModel):
    type: Optional[Literal["media"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class SingleChoiceBlockUpdate(BaseModel):
    type: Optional[Literal["single_choice"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class MultipleChoiceBlockUpdate(BaseModel):
    type: Optional[Literal["multiple_choice"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class TextInputBlockUpdate(BaseModel):
    type: Optional[Literal["text_input"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class TextAreaBlockUpdate(BaseModel):
    type: Optional[Literal["text_area"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class FileUploadBlockUpdate(BaseModel):
    type: Optional[Literal["file_upload"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class ExternalLinkBlockUpdate(BaseModel):
    type: Optional[Literal["external_link"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class ChecklistBlockUpdate(BaseModel):
    type: Optional[Literal["checklist"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class CautionBlockUpdate(BaseModel):
    type: Optional[Literal["caution"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class ListBlockUpdate(BaseModel):
    type: Optional[Literal["list"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class DateBlockUpdate(BaseModel):
    type: Optional[Literal["date"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class TimePickerBlockUpdate(BaseModel):
    type: Optional[Literal["time_picker"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class RatingScaleBlockUpdate(BaseModel):
    type: Optional[Literal["rating_scale"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

class VisualAudioBlockUpdate(BaseModel):
    type: Optional[Literal["visual_audio"]] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[Dict[str, Any]] = None
    order_index: Optional[int] = None

