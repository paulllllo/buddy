from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import uuid
from app.models.stage_template import StageTemplate
from app.services.content_type_service import ContentTypeService


class StageTemplateService:
    """Service for managing stage templates"""
    
    @staticmethod
    def seed_stage_templates(db: Session) -> List[StageTemplate]:
        """Seed the database with default stage templates"""
        templates_data = [
            {
                "name": "Welcome Introduction",
                "description": "Welcome new hires with company introduction",
                "type": "introduction",
                "default_content": [
                    {
                        "type": "header",
                        "config": {
                            "label": "Welcome Header",
                            "description": "Main welcome message",
                            "required": False,
                            "validation": {
                                "rules": [
                                    {"type": "max_length", "value": 100, "field": "title"}
                                ],
                                "messages": {
                                    "title_max_length": "Title must be less than 100 characters"
                                }
                            },
                            "display": {
                                "width": "full",
                                "order": 1,
                                "visibility": "always"
                            },
                            "style": {
                                "title_size": "h1",
                                "alignment": "center",
                                "color": "primary"
                            }
                        },
                        "content": {
                            "title": "Welcome to Our Company!",
                            "subtitle": "We're excited to have you join our team"
                        }
                    },
                    {
                        "type": "description",
                        "config": {
                            "label": "Welcome Description",
                            "description": "Introduction text",
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
                        },
                        "content": {
                            "text": "This onboarding process will help you get familiar with our company culture, policies, and procedures. Take your time to complete each section thoroughly."
                        }
                    },
                    {
                        "type": "external_link",
                        "config": {
                            "label": "Company Handbook",
                            "description": "Link to company handbook",
                            "required": False,
                            "validation": {
                                "rules": [
                                    {"type": "url", "field": "url"}
                                ],
                                "messages": {
                                    "url": "Please enter a valid URL"
                                }
                            },
                            "display": {
                                "width": "full",
                                "order": 3,
                                "visibility": "always"
                            },
                            "link": {
                                "open_in_new_tab": True,
                                "show_icon": True,
                                "track_clicks": True
                            }
                        },
                        "content": {
                            "title": "Company Handbook",
                            "url": "/handbook",
                            "description": "Access the complete employee handbook"
                        }
                    }
                ],
                "default_config": {
                    "estimated_time": 10,
                    "required": True,
                    "allow_skip": False
                }
            },
            {
                "name": "Company Policies",
                "description": "Review important company policies and procedures",
                "type": "policies",
                "default_content": [
                    {
                        "type": "header",
                        "config": {
                            "label": "Policies Header",
                            "description": "Policies section header",
                            "required": False,
                            "validation": {
                                "rules": [
                                    {"type": "max_length", "value": 100, "field": "title"}
                                ],
                                "messages": {
                                    "title_max_length": "Title must be less than 100 characters"
                                }
                            },
                            "display": {
                                "width": "full",
                                "order": 1,
                                "visibility": "always"
                            },
                            "style": {
                                "title_size": "h2",
                                "alignment": "left",
                                "color": "primary"
                            }
                        },
                        "content": {
                            "title": "Company Policies",
                            "subtitle": "Please review the following policies carefully"
                        }
                    },
                    {
                        "type": "checklist",
                        "config": {
                            "label": "Policy Acknowledgment",
                            "description": "Confirm policy understanding",
                            "required": True,
                            "validation": {
                                "rules": [
                                    {"type": "required", "field": "checked_items"},
                                    {"type": "min_selections", "value": 4, "field": "checked_items"}
                                ],
                                "messages": {
                                    "required": "Please acknowledge all policies",
                                    "min_selections": "Please check all required items"
                                }
                            },
                            "display": {
                                "width": "full",
                                "order": 2,
                                "visibility": "always"
                            },
                            "checklist": {
                                "allow_partial": False,
                                "show_progress": True,
                                "auto_save": True
                            }
                        },
                        "content": {
                            "title": "Policy Acknowledgment",
                            "description": "Please check each item to confirm you have read and understood the policies",
                            "items": [
                                {"id": "1", "text": "I have read and understood the Employee Handbook", "required": True},
                                {"id": "2", "text": "I agree to follow the Code of Conduct", "required": True},
                                {"id": "3", "text": "I understand the Data Privacy Policy", "required": True},
                                {"id": "4", "text": "I acknowledge the Workplace Safety Guidelines", "required": True},
                                {"id": "5", "text": "I understand the Anti-Harassment Policy", "required": False}
                            ]
                        }
                    }
                ],
                "default_config": {
                    "estimated_time": 15,
                    "required": True,
                    "allow_skip": False
                }
            },
            {
                "name": "Personal Information",
                "description": "Collect essential personal and employment information",
                "type": "forms",
                "default_content": [
                    {
                        "type": "header",
                        "config": {
                            "label": "Personal Info Header",
                            "description": "Personal information section",
                            "required": False,
                            "validation": {
                                "rules": [
                                    {"type": "max_length", "value": 100, "field": "title"}
                                ],
                                "messages": {
                                    "title_max_length": "Title must be less than 100 characters"
                                }
                            },
                            "display": {
                                "width": "full",
                                "order": 1,
                                "visibility": "always"
                            },
                            "style": {
                                "title_size": "h2",
                                "alignment": "left",
                                "color": "primary"
                            }
                        },
                        "content": {
                            "title": "Personal Information",
                            "subtitle": "Please provide your personal information for our records"
                        }
                    },
                    {
                        "type": "text_input",
                        "config": {
                            "label": "Full Legal Name",
                            "description": "Enter your full legal name",
                            "required": True,
                            "validation": {
                                "rules": [
                                    {"type": "required", "field": "value"},
                                    {"type": "min_length", "value": 2, "field": "value"},
                                    {"type": "max_length", "value": 100, "field": "value"}
                                ],
                                "messages": {
                                    "required": "Full name is required",
                                    "min_length": "Name must be at least 2 characters",
                                    "max_length": "Name must be less than 100 characters"
                                }
                            },
                            "display": {
                                "width": "full",
                                "order": 2,
                                "visibility": "always"
                            },
                            "input": {
                                "type": "text",
                                "placeholder": "Enter your full legal name",
                                "autocomplete": "name"
                            }
                        },
                        "content": {
                            "label": "Full Legal Name"
                        }
                    },
                    {
                        "type": "text_input",
                        "config": {
                            "label": "Email Address",
                            "description": "Enter your email address",
                            "required": True,
                            "validation": {
                                "rules": [
                                    {"type": "required", "field": "value"},
                                    {"type": "email", "field": "value"}
                                ],
                                "messages": {
                                    "required": "Email address is required",
                                    "email": "Please enter a valid email address"
                                }
                            },
                            "display": {
                                "width": "full",
                                "order": 3,
                                "visibility": "always"
                            },
                            "input": {
                                "type": "email",
                                "placeholder": "Enter your email address",
                                "autocomplete": "email"
                            }
                        },
                        "content": {
                            "label": "Email Address"
                        }
                    },
                    {
                        "type": "date",
                        "config": {
                            "label": "Date of Birth",
                            "description": "Select your date of birth",
                            "required": True,
                            "validation": {
                                "rules": [
                                    {"type": "required", "field": "date"},
                                    {"type": "max_date", "value": "today", "field": "date"}
                                ],
                                "messages": {
                                    "required": "Date of birth is required",
                                    "max_date": "Date cannot be in the future"
                                }
                            },
                            "display": {
                                "width": "half",
                                "order": 4,
                                "visibility": "always"
                            },
                            "date": {
                                "format": "MM/DD/YYYY",
                                "allow_past": True,
                                "allow_future": False,
                                "show_calendar": True,
                                "placeholder": "Select date of birth"
                            }
                        },
                        "content": {
                            "label": "Date of Birth"
                        }
                    }
                ],
                "default_config": {
                    "estimated_time": 10,
                    "required": True,
                    "allow_skip": False
                }
            },
            {
                "name": "Emergency Contacts",
                "description": "Collect emergency contact information",
                "type": "forms",
                "default_content": [
                    {
                        "type": "header",
                        "config": {
                            "label": "Emergency Contacts Header",
                            "description": "Emergency contact information",
                            "required": False,
                            "validation": {
                                "rules": [
                                    {"type": "max_length", "value": 100, "field": "title"}
                                ],
                                "messages": {
                                    "title_max_length": "Title must be less than 100 characters"
                                }
                            },
                            "display": {
                                "width": "full",
                                "order": 1,
                                "visibility": "always"
                            },
                            "style": {
                                "title_size": "h2",
                                "alignment": "left",
                                "color": "primary"
                            }
                        },
                        "content": {
                            "title": "Emergency Contacts",
                            "subtitle": "Please provide emergency contact information"
                        }
                    },
                    {
                        "type": "text_input",
                        "config": {
                            "label": "Emergency Contact Name",
                            "description": "Enter emergency contact name",
                            "required": True,
                            "validation": {
                                "rules": [
                                    {"type": "required", "field": "value"},
                                    {"type": "min_length", "value": 2, "field": "value"},
                                    {"type": "max_length", "value": 100, "field": "value"}
                                ],
                                "messages": {
                                    "required": "Emergency contact name is required",
                                    "min_length": "Name must be at least 2 characters",
                                    "max_length": "Name must be less than 100 characters"
                                }
                            },
                            "display": {
                                "width": "full",
                                "order": 2,
                                "visibility": "always"
                            },
                            "input": {
                                "type": "text",
                                "placeholder": "Enter emergency contact name",
                                "autocomplete": "name"
                            }
                        },
                        "content": {
                            "label": "Emergency Contact Name"
                        }
                    },
                    {
                        "type": "text_input",
                        "config": {
                            "label": "Emergency Contact Phone",
                            "description": "Enter emergency contact phone number",
                            "required": True,
                            "validation": {
                                "rules": [
                                    {"type": "required", "field": "value"},
                                    {"type": "pattern", "value": "^[+]?[0-9\\s\\-\\(\\)]+$", "field": "value"}
                                ],
                                "messages": {
                                    "required": "Emergency contact phone is required",
                                    "pattern": "Please enter a valid phone number"
                                }
                            },
                            "display": {
                                "width": "full",
                                "order": 3,
                                "visibility": "always"
                            },
                            "input": {
                                "type": "tel",
                                "placeholder": "Enter emergency contact phone",
                                "autocomplete": "tel"
                            }
                        },
                        "content": {
                            "label": "Emergency Contact Phone"
                        }
                    }
                ],
                "default_config": {
                    "estimated_time": 5,
                    "required": True,
                    "allow_skip": False
                }
            },
            {
                "name": "Document Upload",
                "description": "Upload required documents and forms",
                "type": "documents",
                "default_content": [
                    {
                        "type": "header",
                        "config": {
                            "label": "Documents Header",
                            "description": "Document upload section",
                            "required": False,
                            "validation": {
                                "rules": [
                                    {"type": "max_length", "value": 100, "field": "title"}
                                ],
                                "messages": {
                                    "title_max_length": "Title must be less than 100 characters"
                                }
                            },
                            "display": {
                                "width": "full",
                                "order": 1,
                                "visibility": "always"
                            },
                            "style": {
                                "title_size": "h2",
                                "alignment": "left",
                                "color": "primary"
                            }
                        },
                        "content": {
                            "title": "Required Documents",
                            "subtitle": "Please upload the following required documents"
                        }
                    },
                    {
                        "type": "file_upload",
                        "config": {
                            "label": "Government ID",
                            "description": "Upload a copy of your government-issued ID",
                            "required": True,
                            "validation": {
                                "rules": [
                                    {"type": "required", "field": "files"},
                                    {"type": "file_type", "value": ["image/jpeg", "image/png", "application/pdf"], "field": "files"},
                                    {"type": "file_size", "value": 5242880, "field": "files"}
                                ],
                                "messages": {
                                    "required": "Government ID is required",
                                    "file_type": "Only JPG, PNG, and PDF files are allowed",
                                    "file_size": "File must be less than 5MB"
                                }
                            },
                            "display": {
                                "width": "full",
                                "order": 2,
                                "visibility": "always"
                            },
                            "upload": {
                                "multiple": False,
                                "drag_drop": True,
                                "preview": True,
                                "progress": True
                            }
                        },
                        "content": {
                            "label": "Government ID",
                            "description": "Upload a clear copy of your government-issued ID (driver's license, passport, etc.)"
                        }
                    },
                    {
                        "type": "file_upload",
                        "config": {
                            "label": "Resume/CV",
                            "description": "Upload your current resume or CV",
                            "required": True,
                            "validation": {
                                "rules": [
                                    {"type": "required", "field": "files"},
                                    {"type": "file_type", "value": ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"], "field": "files"},
                                    {"type": "file_size", "value": 5242880, "field": "files"}
                                ],
                                "messages": {
                                    "required": "Resume/CV is required",
                                    "file_type": "Only PDF and Word documents are allowed",
                                    "file_size": "File must be less than 5MB"
                                }
                            },
                            "display": {
                                "width": "full",
                                "order": 3,
                                "visibility": "always"
                            },
                            "upload": {
                                "multiple": False,
                                "drag_drop": True,
                                "preview": True,
                                "progress": True
                            }
                        },
                        "content": {
                            "label": "Resume/CV",
                            "description": "Upload your current resume or curriculum vitae"
                        }
                    }
                ],
                "default_config": {
                    "estimated_time": 10,
                    "required": True,
                    "allow_skip": False
                }
            }
        ]
        
        created_templates = []
        for data in templates_data:
            # Check if template already exists
            existing = db.query(StageTemplate).filter(StageTemplate.name == data["name"]).first()
            if not existing:
                template = StageTemplate(**data)
                db.add(template)
                created_templates.append(template)
        
        db.commit()
        return created_templates
    
    @staticmethod
    def get_all_templates(db: Session, public_only: bool = True) -> List[StageTemplate]:
        """Get all stage templates"""
        query = db.query(StageTemplate)
        if public_only:
            query = query.filter(StageTemplate.is_public == True)
        return query.all()
    
    @staticmethod
    def get_template_by_id(db: Session, template_id: str) -> Optional[StageTemplate]:
        """Get stage template by ID"""
        template_uuid = uuid.UUID(template_id)
        return db.query(StageTemplate).filter(StageTemplate.id == template_uuid).first()
    
    @staticmethod
    def get_templates_by_type(db: Session, template_type: str) -> List[StageTemplate]:
        """Get stage templates by type"""
        return db.query(StageTemplate).filter(
            StageTemplate.type == template_type,
            StageTemplate.is_public == True
        ).all()
    
    @staticmethod
    def create_template(
        db: Session,
        name: str,
        description: str,
        template_type: str,
        default_content: List[Dict[str, Any]],
        default_config: Dict[str, Any],
        is_public: bool = True
    ) -> StageTemplate:
        """Create a new stage template"""
        template = StageTemplate(
            name=name,
            description=description,
            type=template_type,
            default_content=default_content,
            default_config=default_config,
            is_public=is_public
        )
        
        db.add(template)
        db.commit()
        db.refresh(template)
        return template 