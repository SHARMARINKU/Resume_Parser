from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
import os


class ResumeProfile(BaseModel):
    """Model for basic profile information"""
    name: str
    location :str
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    current_title: Optional[str] = None
    summary: Optional[str] = None

    # Override __init__ to flatten contact dictionary automatically
    def __init__(self, **data):
        contact = data.pop('contact', {})  # Extract nested contact dict
        if contact:
            data['email'] = contact.get('email')
            data['phone'] = contact.get('phone')
            data['linkedin'] = contact.get('linkedin')
        super().__init__(**data)


class ResumeSkills(BaseModel):
    """Model for skills"""
    skills: List[str]
    # skills: Dict[str, List[str]]


class Skills(BaseModel):
    """Simple skills model for backward compatibility"""
    skills: List[str] = Field(
        ...,
        description="A list of skills extracted from the resume text."
    )


class Education(BaseModel):
    degree: str
    institution: str
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    def __init__(self, **data):
        if 'graduation_date' in data and 'end_date' not in data:
            data['end_date'] = data.pop('graduation_date')
        super().__init__(**data)

class Experience(BaseModel):
    """Model for a work experience entry"""
    company: str
    role: str
    location: Optional[str] = None
    start_date: str
    end_date: str


class ResumeWorkExperience(BaseModel):
    """Model for work experience information"""
    work_experiences: List[Experience]


class WorkDates(BaseModel):
    """Model for work dates information"""
    oldest_working_date: str
    newest_working_date: str
    total_experience: Optional[str] = None


class Resume(BaseModel):
    """A complete resume with all extracted information."""
    # Profile information
    full_resume: str
    # name: Optional[str] = None
    # contact_number: Optional[str] = None
    # email: Optional[str] = None
    #
    # # Skills
    # skills: List[str] = Field(default_factory=list)
    #
    # # Education
    # educations: List[Education] = Field(default_factory=list)
    #
    # # Work Experience
    # work_experiences: List[Experience] = Field(default_factory=list)
    #
    # # Years of Experience
    # YoE: Optional[str] = None
    #
    # # File information
    # file_path: Optional[str] = None
    # file_name: Optional[str] = None
    #
    # # Token usage information
    # token_usage: Dict[str, Any] = Field(default_factory=dict)
    #
    # # Plugin data for custom extractors
    # plugin_data: Dict[str, Any] = Field(default_factory=dict)
    #
