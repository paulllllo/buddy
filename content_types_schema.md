# Dynamic Content Types Schema

## Overview

This document defines a structured JSON schema for content types that can be used consistently across:
1. **Admin Portal:** Content setup and configuration
2. **New Hire Portal:** Content rendering and data collection
3. **Backend:** Validation, storage, and processing

**Note:** All rendering is handled by frontend components. The backend only stores and validates the JSON configuration data.

## Admin Config Validation vs New-Hire User Input Validation

There are two distinct validation concerns:
- Admin Config Validation: Ensures that a content block’s configuration and authored content are structurally sound when an admin creates/edits blocks. This is handled by backend services such as [`ContentService.validate_content_block()`](backend/app/services/content_service.py:140).
- New-Hire User Input Validation: Ensures that data submitted by a new hire for a content block conforms to the rules defined in the block’s admin configuration and authored content. This path is handled inside onboarding service by a dedicated validator.

The onboarding path previously used the admin config validator for user inputs. This has been corrected with a new method in the onboarding service that validates user input specifically against config rules and the authored content of the block.

## Core Content Type Structure

```json
{
  "type": "content_type_name",
  "config": {
    "label": "Human-readable label",
    "description": "Optional description",
    "required": true/false,
    "validation": {
      "rules": [...],
      "messages": {...}
    },
    "display": {
      "width": "full|half|third",
      "order": 1,
      "visibility": "always|conditional"
    },
    "content_specific_config": {...}
  },
  "content": {
    "value": "actual content data",
    "metadata": {...}
  }
}
```

---

## Content Type Definitions

### 1. Header Content Type

```json
{
  "type": "header",
  "config": {
    "label": "Header",
    "description": "Section header with title and optional subtitle",
    "required": false,
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
      "title_size": "h1|h2|h3|h4",
      "alignment": "left|center|right",
      "color": "primary|secondary|accent|custom"
    }
  },
  "content": {
    "title": "Welcome to Our Company",
    "subtitle": "We're excited to have you on board!",
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 2. Description Content Type

```json
{
  "type": "description",
  "config": {
    "label": "Description",
    "description": "Rich text content with formatting",
    "required": false,
    "validation": {
      "rules": [
        {"type": "max_length", "value": 2000, "field": "text"}
      ],
      "messages": {
        "text_max_length": "Description must be less than 2000 characters"
      }
    },
    "display": {
      "width": "full|half",
      "order": 2,
      "visibility": "always"
    },
    "formatting": {
      "allow_bold": true,
      "allow_italic": true,
      "allow_links": true,
      "allow_lists": true
    }
  },
  "content": {
    "text": "This is a rich text description with <strong>bold</strong> and <em>italic</em> formatting.",
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 3. Media Content Type

```json
{
  "type": "media",
  "config": {
    "label": "Media",
    "description": "Image, video, or document display",
    "required": false,
    "validation": {
      "rules": [
        {"type": "file_type", "value": ["image/jpeg", "image/png", "image/gif", "image/webp", "video/mp4", "video/webm", "application/pdf"], "field": "file"},
        {"type": "file_size", "value": 10485760, "field": "file"} // 10MB
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
      "type": "image|video|document",
      "autoplay": false,
      "controls": true,
      "caption": true,
      "lightbox": true,
      "download": false
    }
  },
  "content": {
    "file_url": "https://s3.amazonaws.com/bucket/file.jpg",
    "caption": "Company office building",
    "alt_text": "Modern office building with glass facade",
    "metadata": {
      "file_size": 2048576,
      "file_type": "image/jpeg",
      "dimensions": {"width": 1920, "height": 1080},
      "created_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 4. Single Choice Content Type

```json
{
  "type": "single_choice",
  "config": {
    "label": "Single Choice Question",
    "description": "Multiple choice question with single answer",
    "required": true,
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
      "width": "full|half",
      "order": 4,
      "visibility": "always"
    },
    "question": {
      "allow_other": false,
      "randomize_options": false,
      "show_results": false
    }
  },
  "content": {
    "question": "What is your preferred communication style?",
    "options": [
      {"id": "1", "text": "Email", "value": "email"},
      {"id": "2", "text": "Phone", "value": "phone"},
      {"id": "3", "text": "Video call", "value": "video"},
      {"id": "4", "text": "In-person", "value": "in_person"}
    ],
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 5. Multiple Choice Content Type

```json
{
  "type": "multiple_choice",
  "config": {
    "label": "Multiple Choice Question",
    "description": "Multiple choice question with multiple answers",
    "required": true,
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
      "allow_other": true,
      "other_label": "Other (please specify)",
      "randomize_options": false,
      "show_results": false
    }
  },
  "content": {
    "question": "Which benefits are most important to you?",
    "options": [
      {"id": "1", "text": "Health insurance", "value": "health"},
      {"id": "2", "text": "Dental insurance", "value": "dental"},
      {"id": "3", "text": "Vision insurance", "value": "vision"},
      {"id": "4", "text": "401(k) matching", "value": "401k"},
      {"id": "5", "text": "Flexible work hours", "value": "flexible"},
      {"id": "6", "text": "Remote work options", "value": "remote"}
    ],
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 6. Text Input Content Type

```json
{
  "type": "text_input",
  "config": {
    "label": "Text Input",
    "description": "Single line text input field",
    "required": true,
    "validation": {
      "rules": [
        {"type": "required", "field": "value"},
        {"type": "min_length", "value": 2, "field": "value"},
        {"type": "max_length", "value": 100, "field": "value"},
        {"type": "pattern", "value": "^[a-zA-Z\\s]+$", "field": "value"}
      ],
      "messages": {
        "required": "This field is required",
        "min_length": "Must be at least 2 characters",
        "max_length": "Must be less than 100 characters",
        "pattern": "Only letters and spaces allowed"
      }
    },
    "display": {
      "width": "full|half",
      "order": 6,
      "visibility": "always"
    },
    "input": {
      "type": "text|email|tel|url|number",
      "placeholder": "Enter your answer",
      "autocomplete": "name|email|tel|off"
    }
  },
  "content": {
    "label": "Full Name",
    "placeholder": "Enter your full name",
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 7. Text Area Content Type

```json
{
  "type": "text_area",
  "config": {
    "label": "Text Area",
    "description": "Multi-line text input field",
    "required": true,
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
      "resizable": true
    }
  },
  "content": {
    "label": "Tell us about yourself",
    "placeholder": "Please share a brief introduction about yourself...",
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 8. File Upload Content Type

```json
{
  "type": "file_upload",
  "config": {
    "label": "File Upload",
    "description": "Upload documents or images",
    "required": true,
    "validation": {
      "rules": [
        {"type": "required", "field": "files"},
        {"type": "file_type", "value": ["application/pdf", "image/jpeg", "image/png"], "field": "files"},
        {"type": "file_size", "value": 5242880, "field": "files"}, // 5MB
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
      "multiple": true,
      "drag_drop": true,
      "preview": true,
      "progress": true
    }
  },
  "content": {
    "label": "Upload Required Documents",
    "description": "Please upload your ID, resume, and any other required documents",
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 9. External Link Content Type

```json
{
  "type": "external_link",
  "config": {
    "label": "External Link",
    "description": "Link to external resources",
    "required": false,
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
      "open_in_new_tab": true,
      "show_icon": true,
      "track_clicks": true
    }
  },
  "content": {
    "title": "Employee Handbook",
    "url": "https://company.com/handbook",
    "description": "Access the complete employee handbook",
    "icon": "document",
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 10. Checklist Content Type

```json
{
  "type": "checklist",
  "config": {
    "label": "Checklist",
    "description": "Interactive checklist with items",
    "required": true,
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
      "allow_partial": true,
      "show_progress": true,
      "auto_save": true
    }
  },
  "content": {
    "title": "Pre-employment Checklist",
    "description": "Please complete the following items before your start date",
    "items": [
      {"id": "1", "text": "Complete background check", "required": true},
      {"id": "2", "text": "Submit tax forms", "required": true},
      {"id": "3", "text": "Review company policies", "required": false},
      {"id": "4", "text": "Set up direct deposit", "required": true},
      {"id": "5", "text": "Schedule orientation", "required": false}
    ],
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 11. Caution/Warning Content Type

```json
{
  "type": "caution",
  "config": {
    "label": "Caution",
    "description": "Warning or important notice",
    "required": false,
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
      "type": "info|warning|error|success",
      "dismissible": true,
      "icon": true
    }
  },
  "content": {
    "title": "Important Notice",
    "message": "Please ensure all information provided is accurate and complete. False information may result in termination of employment.",
    "type": "warning",
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 12. List Content Type

```json
{
  "type": "list",
  "config": {
    "label": "List",
    "description": "Ordered or unordered list",
    "required": false,
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
      "type": "ordered|unordered",
      "style": "bullet|number|letter|roman"
    }
  },
  "content": {
    "title": "What to Bring on Your First Day",
    "items": [
      "Government-issued photo ID",
      "Social Security card or passport",
      "Bank account information for direct deposit",
      "Emergency contact information",
      "Comfortable clothing for orientation"
    ],
    "type": "unordered",
    "style": "bullet",
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 13. Date Content Type

```json
{
  "type": "date",
  "config": {
    "label": "Date Selection",
    "description": "Select a specific date",
    "required": true,
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
      "allow_past": false,
      "allow_future": true,
      "show_calendar": true,
      "placeholder": "Select date"
    }
  },
  "content": {
    "label": "Preferred Start Date",
    "placeholder": "Select your preferred start date",
    "min_date": "today",
    "max_date": "+6months",
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 14. Time Picker Content Type

```json
{
  "type": "time_picker",
  "config": {
    "label": "Time Selection",
    "description": "Select a specific time",
    "required": true,
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
      "format": "12|24",
      "interval": 15,
      "show_seconds": false,
      "timezone": "local|utc"
    }
  },
  "content": {
    "label": "Preferred Interview Time",
    "placeholder": "Select your preferred interview time",
    "min_time": "09:00",
    "max_time": "17:00",
    "interval": 30,
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 15. Rating/Scale Content Type

```json
{
  "type": "rating_scale",
  "config": {
    "label": "Rating Scale",
    "description": "Rate something on a scale",
    "required": true,
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
      "type": "stars|numbers|emojis|slider",
      "scale": 5,
      "show_labels": true,
      "show_value": true,
      "allow_half": false
    }
  },
  "content": {
    "question": "How would you rate your experience with our hiring process?",
    "scale": 5,
    "labels": ["Poor", "Fair", "Good", "Very Good", "Excellent"],
    "description": "Please rate your overall experience from 1 to 5",
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

### 16. Visual or Audio Content Type

```json
{
  "type": "visual_audio",
  "config": {
    "label": "Visual or Audio Content",
    "description": "Interactive visual or audio content with responses",
    "required": true,
    "validation": {
      "rules": [
        {"type": "required", "field": "response"},
        {"type": "file_type", "value": ["audio/wav", "audio/mp3", "audio/m4a", "video/mp4", "video/webm"], "field": "recording"},
        {"type": "file_size", "value": 52428800, "field": "recording"} // 50MB
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
      "type": "audio|video|both",
      "recording": true,
      "playback": true,
      "transcription": true,
      "max_duration": 300 // 5 minutes
    }
  },
  "content": {
    "title": "Video Introduction",
    "prompt": "Please record a brief video introducing yourself and explaining why you're interested in this position.",
    "instructions": "Speak clearly and maintain eye contact with the camera. Keep your response under 2 minutes.",
    "max_duration": 120,
    "allow_retakes": true,
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
}
```

---

## New-Hire User Input Validation (Backend)

A dedicated method now validates new-hire submitted data for each content block type using its admin-config and authored content (e.g., option lists).

- Service method: [`OnboardingSessionService.validate_user_input_data()`](backend/app/services/onboarding_service.py:482)
- Integration point: [`OnboardingSessionService.complete_content_block()`](backend/app/services/onboarding_service.py:284) now calls the user-input validator instead of the admin config validator.

Uniform validation principles across input-capable content types:
- required: If config.required is true, the relevant user input field must be present and non-empty.
- membership: For selectable inputs, selected IDs must exist in authored content options/items.
- ranges: Enforce min/max selections, min/max values, min/max dates/times where applicable.
- patterns and length: Enforce min_length, max_length, and pattern for text inputs where rules exist.
- files: Enforce allowed file_type(s), file_size limit(s), and max_files where rules exist.

Display-only content types:
- header, description, media, external_link, list, caution do not accept user input. If these are marked required, validation rejects completion with a descriptive error.


## User Input Schemas (Conceptual)

While the API currently accepts a generic payload for data submission, the validator expects a uniform shape per content type. Below are the normalized fields for each input-capable type:
- single_choice: { "answer": "optionId" }
- multiple_choice: { "answers": ["optionId1", "optionId2", ...] }
- text_input: { "value": "string" }
- text_area: { "value": "string" }
- file_upload: { "files": [{ "file_url": "https://...", "file_type": "mime/type", "file_size": 12345, "file_name": "optional.ext" }, ...] }
- checklist: { "checked_items": ["itemId1", "itemId2", ...] }
- date: { "date": "YYYY-MM-DD" or ISO datetime string }
- time_picker: { "time": "HH:MM" in 24h format }
- rating_scale: { "rating": 1..N }
- visual_audio: { "response": "string optional", "recording": { "file_url": "...", "file_type": "mime", "file_size": 12345, "file_name": "optional" } optional }

This conceptual mapping provides uniformity for client submissions even without strict Pydantic models for user inputs. The backend validator applies the rules defined in the admin config to these normalized fields.


## Implementation Strategy

### Backend Implementation

```python
# content_types/validators.py
class ContentValidator:
    @staticmethod
    def validate_required(value: any, required: bool) -> ValidationResult:
        """Validate required fields"""
        pass
    
    @staticmethod
    def validate_length(value: str, min_length: int, max_length: int) -> ValidationResult:
        """Validate text length constraints"""
        pass
    
    @staticmethod
    def validate_file(file: UploadFile, allowed_types: list, max_size: int) -> ValidationResult:
        """Validate file uploads"""
        pass
    
    @staticmethod
    def validate_date(date: str, min_date: str, max_date: str) -> ValidationResult:
        """Validate date constraints"""
        pass
    
    @staticmethod
    def validate_time(time: str, min_time: str, max_time: str) -> ValidationResult:
        """Validate time constraints"""
        pass

# content_types/registry.py
class ContentTypeRegistry:
    def __init__(self):
        self.types = {}
    
    def register_validation_rules(self, content_type: str, rules: dict):
        """Register validation rules for content types"""
        self.types[content_type] = rules
    
    def get_validation_rules(self, content_type: str) -> dict:
        """Get validation rules for a content type"""
        return self.types.get(content_type, {})
    
    def get_all_content_types(self) -> list:
        """Get list of all available content types"""
        return list(self.types.keys())

# models/content_block.py
class ContentBlock(Base):
    id = Column(UUID, primary_key=True)
    stage_id = Column(UUID, ForeignKey("stages.id"), nullable=False)
    type = Column(String, nullable=False)  # content type name
    config = Column(JSONB, nullable=False)  # validation and display config
    content = Column(JSONB, nullable=False)  # actual content data
    order_index = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Frontend Implementation

```typescript
// content-types/types.ts
interface ContentTypeConfig {
  type: string;
  config: {
    label: string;
    description?: string;
    required: boolean;
    validation: ValidationRules;
    display: DisplayConfig;
    [key: string]: any;
  };
  content: {
    [key: string]: any;
    metadata: Metadata;
  };
}

// content-types/components.tsx
// React components for each content type
const HeaderComponent: React.FC<ContentTypeProps> = ({ config, content, mode, onChange }) => {
  // Render header content type
};

const DescriptionComponent: React.FC<ContentTypeProps> = ({ config, content, mode, onChange }) => {
  // Render description content type
};

const SingleChoiceComponent: React.FC<ContentTypeProps> = ({ config, content, mode, onChange }) => {
  // Render single choice content type
};

// ... more components for each content type

// content-types/renderer.tsx
class ContentRenderer {
  private static componentMap = new Map<string, React.ComponentType<ContentTypeProps>>([
    ['header', HeaderComponent],
    ['description', DescriptionComponent],
    ['single_choice', SingleChoiceComponent],
    ['multiple_choice', MultipleChoiceComponent],
    ['text_input', TextInputComponent],
    ['text_area', TextAreaComponent],
    ['file_upload', FileUploadComponent],
    ['external_link', ExternalLinkComponent],
    ['checklist', ChecklistComponent],
    ['caution', CautionComponent],
    ['list', ListComponent],
    ['date', DateComponent],
    ['time_picker', TimePickerComponent],
    ['rating_scale', RatingScaleComponent],
    ['visual_audio', VisualAudioComponent],
    ['media', MediaComponent]
  ]);

  static render(contentType: ContentTypeConfig, mode: 'admin' | 'new_hire'): JSX.Element {
    const Component = this.componentMap.get(contentType.type);
    if (!Component) {
      return <div>Unknown content type: {contentType.type}</div>;
    }
    
    return (
      <Component
        config={contentType.config}
        content={contentType.content}
        mode={mode}
        onChange={(data) => this.handleChange(contentType, data)}
      />
    );
  }

  static validate(contentType: ContentTypeConfig, userInput: any): ValidationResult {
    // Client-side validation using config rules
    const rules = contentType.config.validation.rules;
    return this.validateRules(rules, userInput);
  }

  private static validateRules(rules: ValidationRule[], input: any): ValidationResult {
    // Implement validation logic based on rules
  }
}

// content-types/registry.ts
class ContentTypeRegistry {
  private static contentTypes = new Map<string, ContentTypeConfig>();
  
  static register(type: ContentTypeConfig): void {
    this.contentTypes.set(type.type, type);
  }
  
  static getType(name: string): ContentTypeConfig | undefined {
    return this.contentTypes.get(name);
  }
  
  static getAllTypes(): ContentTypeConfig[] {
    return Array.from(this.contentTypes.values());
  }
  
  static getAvailableTypes(): string[] {
    return Array.from(this.contentTypes.keys());
  }
}
```

### Database Storage

```sql
-- content_blocks table
CREATE TABLE content_blocks (
    id UUID PRIMARY KEY,
    stage_id UUID REFERENCES stages(id),
    type VARCHAR(50) NOT NULL,
    config JSONB NOT NULL,
    content JSONB NOT NULL,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index for efficient querying
CREATE INDEX idx_content_blocks_stage_id ON content_blocks(stage_id);
CREATE INDEX idx_content_blocks_type ON content_blocks(type);
```

### API Endpoints

```python
# api/content_types.py
@router.get("/content-types")
async def get_content_types():
    """Get all available content types for admin portal"""
    return content_type_registry.get_all_content_types()

@router.post("/content-types/{type_name}/validate")
async def validate_content_type_data(
    type_name: str,
    data: dict
):
    """Validate admin config/content (admin-side)"""
    rules = content_type_registry.get_validation_rules(type_name)
    return ContentValidator.validate_data(rules, data)

@router.get("/content-types/{type_name}/config")
async def get_content_type_config(type_name: str):
    """Get default configuration for a content type"""
    return content_type_registry.get_content_type_config(type_name)

# api/onboarding.py (user-side)
@router.post("/{session_token}/stages/{stage_id}/content-blocks/{content_block_id}/complete")
async def complete_content_block(...):
    """
    Complete a content block with new-hire data. The service will:
      1) Fetch the block and its config/content.
      2) Validate user data using OnboardingSessionService.validate_user_input_data.
      3) Persist progress on success.
    """
```

---

## Benefits of This Approach

1. **Frontend-Driven Rendering:** All UI rendering handled by React components
2. **Backend Data Storage:** Backend only stores and validates JSON configuration
3. **Consistency:** Same schema used across admin and new hire portals
4. **Extensibility:** Easy to add new content types by creating new React components
5. **Validation:** Both client-side and server-side validation
6. **Flexibility:** JSON-based configuration allows complex setups
7. **Type Safety:** Strong typing with TypeScript/Python
8. **Reusability:** React components can be shared between admin and new hire contexts
9. **Maintainability:** Clear separation between data (backend) and presentation (frontend)
10. **Performance:** No server-side rendering, faster client-side updates

## Architecture Flow

1. **Admin Portal:** 
   - Fetches content type configurations from backend
   - Uses React components to render setup interfaces
   - Saves JSON configuration to backend

2. **New Hire Portal:**
   - Fetches content blocks with JSON config from backend
   - Uses same React components to render data collection interfaces
   - Validates user input against config rules
   - Submits collected data to backend

3. **Backend:**
   - Stores JSON configuration and content data
   - Validates incoming data against stored rules
   - Provides content type metadata and validation rules

This structured approach ensures that content types work consistently across all parts of the application while maintaining flexibility for future enhancements. 