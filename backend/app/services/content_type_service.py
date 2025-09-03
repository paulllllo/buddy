from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.content_type import ContentType


class ContentTypeService:
    """Service for managing content types"""
    
    @staticmethod
    def seed_content_types(db: Session) -> List[ContentType]:
        """Seed the database with default content types"""
        content_types_data = [
            {
                "name": "header",
                "display_name": "Header",
                "description": "Large text header for titles and sections",
                "category": "text",
                "default_config": {
                    "label": "Header",
                    "description": "Section header with title and optional subtitle",
                    "required": False,
                    "validation": {
                        "rules": [
                            {"type": "max_length", "value": 100, "field": "title"},
                            {"type": "max_length", "value": 200, "field": "subtitle"}
                        ],
                        "messages": {
                            "title_max_length": "Title must be less than 100 characters",
                            "subtitle_max_length": "Subtitle must be less than 200 characters"
                        }
                    },
                    "display": {
                        "width": "full",
                        "order": 1,
                        "visibility": "always"
                    },
                    "style": {
                        "title_size": "h1",
                        "alignment": "left",
                        "color": "primary"
                    }
                }
            },
            {
                "name": "description",
                "display_name": "Description",
                "description": "Regular text content for descriptions and explanations",
                "category": "text",
                "default_config": {
                    "label": "Description",
                    "description": "Rich text content with formatting",
                    "required": False,
                    "validation": {
                        "rules": [
                            {"type": "max_length", "value": 2000, "field": "text"}
                        ],
                        "messages": {
                            "text_max_length": "Description must be less than 2000 characters"
                        }
                    },
                    "display": {
                        "width": "full",
                        "order": 2,
                        "visibility": "always"
                    },
                    "formatting": {
                        "allow_bold": True,
                        "allow_italic": True,
                        "allow_links": True,
                        "allow_lists": True
                    }
                }
            },
            {
                "name": "media",
                "display_name": "Media",
                "description": "Images, videos, and other media content",
                "category": "media",
                "default_config": {
                    "label": "Media",
                    "description": "Image, video, or document display",
                    "required": False,
                    "validation": {
                        "rules": [
                            {"type": "file_type", "value": ["image/jpeg", "image/png", "image/gif", "image/webp", "video/mp4", "video/webm", "application/pdf"], "field": "file"},
                            {"type": "file_size", "value": 10485760, "field": "file"}
                        ],
                        "messages": {
                            "file_type": "Only images, videos, and PDFs are allowed",
                            "file_size": "File must be less than 10MB"
                        }
                    },
                    "display": {
                        "width": "full",
                        "order": 3,
                        "visibility": "always"
                    },
                    "media": {
                        "type": "image",
                        "autoplay": False,
                        "controls": True,
                        "caption": True,
                        "lightbox": True,
                        "download": False
                    }
                }
            },
            {
                "name": "single_choice",
                "display_name": "Single Choice",
                "description": "Multiple choice question with single answer",
                "category": "form",
                "default_config": {
                    "label": "Single Choice Question",
                    "description": "Multiple choice question with single answer",
                    "required": True,
                    "validation": {
                        "rules": [
                            {"type": "required", "field": "answer"},
                            {"type": "min_options", "value": 2, "field": "options"},
                            {"type": "max_options", "value": 10, "field": "options"}
                        ],
                        "messages": {
                            "required": "Please select an answer",
                            "min_options": "At least 2 options are required",
                            "max_options": "Maximum 10 options allowed"
                        }
                    },
                    "display": {
                        "width": "full",
                        "order": 4,
                        "visibility": "always"
                    },
                    "question": {
                        "allow_other": False,
                        "randomize_options": False,
                        "show_results": False
                    }
                }
            },
            {
                "name": "multiple_choice",
                "display_name": "Multiple Choice",
                "description": "Multiple choice question with multiple answers",
                "category": "form",
                "default_config": {
                    "label": "Multiple Choice Question",
                    "description": "Multiple choice question with multiple answers",
                    "required": True,
                    "validation": {
                        "rules": [
                            {"type": "required", "field": "answers"},
                            {"type": "min_selections", "value": 1, "field": "answers"},
                            {"type": "max_selections", "value": 5, "field": "answers"},
                            {"type": "min_options", "value": 2, "field": "options"},
                            {"type": "max_options", "value": 15, "field": "options"}
                        ],
                        "messages": {
                            "required": "Please select at least one answer",
                            "min_selections": "Please select at least one option",
                            "max_selections": "You can select up to 5 options"
                        }
                    },
                    "display": {
                        "width": "full",
                        "order": 5,
                        "visibility": "always"
                    },
                    "question": {
                        "allow_other": True,
                        "other_label": "Other (please specify)",
                        "randomize_options": False,
                        "show_results": False
                    }
                }
            },
            {
                "name": "text_input",
                "display_name": "Text Input",
                "description": "Single line text input field",
                "category": "form",
                "default_config": {
                    "label": "Text Input",
                    "description": "Single line text input field",
                    "required": True,
                    "validation": {
                        "rules": [
                            {"type": "required", "field": "value"},
                            {"type": "min_length", "value": 2, "field": "value"},
                            {"type": "max_length", "value": 100, "field": "value"}
                        ],
                        "messages": {
                            "required": "This field is required",
                            "min_length": "Must be at least 2 characters",
                            "max_length": "Must be less than 100 characters"
                        }
                    },
                    "display": {
                        "width": "full",
                        "order": 6,
                        "visibility": "always"
                    },
                    "input": {
                        "type": "text",
                        "placeholder": "Enter your answer",
                        "autocomplete": "off"
                    }
                }
            },
            {
                "name": "text_area",
                "display_name": "Text Area",
                "description": "Multi-line text input field",
                "category": "form",
                "default_config": {
                    "label": "Text Area",
                    "description": "Multi-line text input field",
                    "required": True,
                    "validation": {
                        "rules": [
                            {"type": "required", "field": "value"},
                            {"type": "min_length", "value": 10, "field": "value"},
                            {"type": "max_length", "value": 1000, "field": "value"}
                        ],
                        "messages": {
                            "required": "This field is required",
                            "min_length": "Must be at least 10 characters",
                            "max_length": "Must be less than 1000 characters"
                        }
                    },
                    "display": {
                        "width": "full",
                        "order": 7,
                        "visibility": "always"
                    },
                    "input": {
                        "rows": 4,
                        "placeholder": "Enter your answer",
                        "resizable": True
                    }
                }
            },
            {
                "name": "file_upload",
                "display_name": "File Upload",
                "description": "File upload field for documents and media",
                "category": "form",
                "default_config": {
                    "label": "File Upload",
                    "description": "Upload documents or images",
                    "required": True,
                    "validation": {
                        "rules": [
                            {"type": "required", "field": "files"},
                            {"type": "file_type", "value": ["application/pdf", "image/jpeg", "image/png"], "field": "files"},
                            {"type": "file_size", "value": 5242880, "field": "files"},
                            {"type": "max_files", "value": 3, "field": "files"}
                        ],
                        "messages": {
                            "required": "Please upload at least one file",
                            "file_type": "Only PDF and image files are allowed",
                            "file_size": "Each file must be less than 5MB",
                            "max_files": "You can upload up to 3 files"
                        }
                    },
                    "display": {
                        "width": "full",
                        "order": 8,
                        "visibility": "always"
                    },
                    "upload": {
                        "multiple": True,
                        "drag_drop": True,
                        "preview": True,
                        "progress": True
                    }
                }
            },
            {
                "name": "external_link",
                "display_name": "External Link",
                "description": "Link to external resources and websites",
                "category": "navigation",
                "default_config": {
                    "label": "External Link",
                    "description": "Link to external resources",
                    "required": False,
                    "validation": {
                        "rules": [
                            {"type": "url", "field": "url"},
                            {"type": "max_length", "value": 200, "field": "title"}
                        ],
                        "messages": {
                            "url": "Please enter a valid URL",
                            "title_max_length": "Title must be less than 200 characters"
                        }
                    },
                    "display": {
                        "width": "full",
                        "order": 9,
                        "visibility": "always"
                    },
                    "link": {
                        "open_in_new_tab": True,
                        "show_icon": True,
                        "track_clicks": True
                    }
                }
            },
            {
                "name": "checklist",
                "display_name": "Checklist",
                "description": "Interactive checklist with checkboxes",
                "category": "form",
                "default_config": {
                    "label": "Checklist",
                    "description": "Interactive checklist with items",
                    "required": True,
                    "validation": {
                        "rules": [
                            {"type": "required", "field": "checked_items"},
                            {"type": "min_selections", "value": 1, "field": "checked_items"},
                            {"type": "min_items", "value": 2, "field": "items"},
                            {"type": "max_items", "value": 20, "field": "items"}
                        ],
                        "messages": {
                            "required": "Please complete at least one item",
                            "min_selections": "Please check at least one item",
                            "min_items": "At least 2 items are required",
                            "max_items": "Maximum 20 items allowed"
                        }
                    },
                    "display": {
                        "width": "full",
                        "order": 10,
                        "visibility": "always"
                    },
                    "checklist": {
                        "allow_partial": True,
                        "show_progress": True,
                        "auto_save": True
                    }
                }
            },
            {
                "name": "caution",
                "display_name": "Caution",
                "description": "Warning or important notice box",
                "category": "text",
                "default_config": {
                    "label": "Caution",
                    "description": "Warning or important notice",
                    "required": False,
                    "validation": {
                        "rules": [
                            {"type": "max_length", "value": 500, "field": "message"}
                        ],
                        "messages": {
                            "message_max_length": "Message must be less than 500 characters"
                        }
                    },
                    "display": {
                        "width": "full",
                        "order": 11,
                        "visibility": "always"
                    },
                    "caution": {
                        "type": "warning",
                        "dismissible": True,
                        "icon": True
                    }
                }
            },
            {
                "name": "list",
                "display_name": "List",
                "description": "Ordered or unordered list",
                "category": "text",
                "default_config": {
                    "label": "List",
                    "description": "Ordered or unordered list",
                    "required": False,
                    "validation": {
                        "rules": [
                            {"type": "min_items", "value": 1, "field": "items"},
                            {"type": "max_items", "value": 50, "field": "items"}
                        ],
                        "messages": {
                            "min_items": "At least one item is required",
                            "max_items": "Maximum 50 items allowed"
                        }
                    },
                    "display": {
                        "width": "full",
                        "order": 12,
                        "visibility": "always"
                    },
                    "list": {
                        "type": "unordered",
                        "style": "bullet"
                    }
                }
            },
            {
                "name": "date",
                "display_name": "Date",
                "description": "Date picker input field",
                "category": "form",
                "default_config": {
                    "label": "Date Selection",
                    "description": "Select a specific date",
                    "required": True,
                    "validation": {
                        "rules": [
                            {"type": "required", "field": "date"},
                            {"type": "min_date", "value": "today", "field": "date"},
                            {"type": "max_date", "value": "+1year", "field": "date"}
                        ],
                        "messages": {
                            "required": "Please select a date",
                            "min_date": "Date cannot be in the past",
                            "max_date": "Date cannot be more than 1 year in the future"
                        }
                    },
                    "display": {
                        "width": "half",
                        "order": 13,
                        "visibility": "always"
                    },
                    "date": {
                        "format": "MM/DD/YYYY",
                        "allow_past": False,
                        "allow_future": True,
                        "show_calendar": True,
                        "placeholder": "Select date"
                    }
                }
            },
            {
                "name": "time_picker",
                "display_name": "Time Picker",
                "description": "Time selection input field",
                "category": "form",
                "default_config": {
                    "label": "Time Selection",
                    "description": "Select a specific time",
                    "required": True,
                    "validation": {
                        "rules": [
                            {"type": "required", "field": "time"},
                            {"type": "min_time", "value": "09:00", "field": "time"},
                            {"type": "max_time", "value": "17:00", "field": "time"}
                        ],
                        "messages": {
                            "required": "Please select a time",
                            "min_time": "Time must be after 9:00 AM",
                            "max_time": "Time must be before 5:00 PM"
                        }
                    },
                    "display": {
                        "width": "half",
                        "order": 14,
                        "visibility": "always"
                    },
                    "time": {
                        "format": "24",
                        "interval": 15,
                        "show_seconds": False,
                        "timezone": "local"
                    }
                }
            },
            {
                "name": "rating_scale",
                "display_name": "Rating Scale",
                "description": "Rating or scale input (1-5, 1-10, etc.)",
                "category": "form",
                "default_config": {
                    "label": "Rating Scale",
                    "description": "Rate something on a scale",
                    "required": True,
                    "validation": {
                        "rules": [
                            {"type": "required", "field": "rating"},
                            {"type": "min_value", "value": 1, "field": "rating"},
                            {"type": "max_value", "value": 5, "field": "rating"}
                        ],
                        "messages": {
                            "required": "Please provide a rating",
                            "min_value": "Rating must be at least 1",
                            "max_value": "Rating cannot exceed 5"
                        }
                    },
                    "display": {
                        "width": "full",
                        "order": 15,
                        "visibility": "always"
                    },
                    "rating": {
                        "type": "stars",
                        "scale": 5,
                        "show_labels": True,
                        "show_value": True,
                        "allow_half": False
                    }
                }
            },
            {
                "name": "visual_audio",
                "display_name": "Visual or Audio Content",
                "description": "Interactive visual or audio content with responses",
                "category": "media",
                "default_config": {
                    "label": "Visual or Audio Content",
                    "description": "Interactive visual or audio content with responses",
                    "required": True,
                    "validation": {
                        "rules": [
                            {"type": "required", "field": "response"},
                            {"type": "file_type", "value": ["audio/wav", "audio/mp3", "audio/m4a", "video/mp4", "video/webm"], "field": "recording"},
                            {"type": "file_size", "value": 52428800, "field": "recording"}
                        ],
                        "messages": {
                            "required": "Please provide your response",
                            "file_type": "Only audio and video files are allowed",
                            "file_size": "Recording must be less than 50MB"
                        }
                    },
                    "display": {
                        "width": "full",
                        "order": 16,
                        "visibility": "always"
                    },
                    "media": {
                        "type": "audio",
                        "recording": True,
                        "playback": True,
                        "transcription": True,
                        "max_duration": 300
                    }
                }
            }
        ]
        
        created_types = []
        for data in content_types_data:
            # Check if content type already exists
            existing = db.query(ContentType).filter(ContentType.name == data["name"]).first()
            if not existing:
                content_type = ContentType(**data)
                db.add(content_type)
                created_types.append(content_type)
        
        db.commit()
        return created_types
    
    @staticmethod
    def get_all_content_types(db: Session, active_only: bool = True) -> List[ContentType]:
        """Get all content types"""
        query = db.query(ContentType)
        if active_only:
            query = query.filter(ContentType.is_active == True)
        return query.all()
    
    @staticmethod
    def get_content_type_by_name(db: Session, name: str) -> Optional[ContentType]:
        """Get content type by name"""
        return db.query(ContentType).filter(
            ContentType.name == name,
            ContentType.is_active == True
        ).first()
    
    @staticmethod
    def get_content_types_by_category(db: Session, category: str) -> List[ContentType]:
        """Get content types by category"""
        return db.query(ContentType).filter(
            ContentType.category == category,
            ContentType.is_active == True
        ).all() 