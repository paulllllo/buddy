from typing import Union, Literal, List, Optional
from pydantic import BaseModel

class FileRef(BaseModel):
    """Represents an uploaded file reference"""
    file_url: str
    file_type: str
    file_size: int
    file_name: Optional[str] = None

class UserInputBase(BaseModel):
    """Base model for all user input types"""
    type: str

class SingleChoiceInput(UserInputBase):
    type: Literal["single_choice"]
    answer: str

class MultipleChoiceInput(UserInputBase):
    type: Literal["multiple_choice"]
    answers: List[str]

class TextInputInput(UserInputBase):
    type: Literal["text_input"]
    value: str

class TextAreaInput(UserInputBase):
    type: Literal["text_area"]
    value: str

class FileUploadInput(UserInputBase):
    type: Literal["file_upload"]
    files: List[FileRef]

class ChecklistInput(UserInputBase):
    type: Literal["checklist"]
    checked_items: List[str]

class DateInput(UserInputBase):
    type: Literal["date"]
    date: str  # ISO 8601 date string

class TimePickerInput(UserInputBase):
    type: Literal["time_picker"]
    time: str  # HH:MM format

class RatingScaleInput(UserInputBase):
    type: Literal["rating_scale"]
    rating: int

class VisualAudioInput(UserInputBase):
    type: Literal["visual_audio"]
    response: Optional[str] = None
    recording: Optional[FileRef] = None

# Discriminated union type for all possible user input types
UserInputSubmission = Union[
    SingleChoiceInput,
    MultipleChoiceInput,
    TextInputInput,
    TextAreaInput,
    FileUploadInput,
    ChecklistInput,
    DateInput,
    TimePickerInput,
    RatingScaleInput,
    VisualAudioInput
]