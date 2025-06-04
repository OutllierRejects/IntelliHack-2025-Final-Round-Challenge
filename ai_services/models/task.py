# ai_services/models/task.py
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Text,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
)
from core.database import Base
import uuid


class TaskType(str, Enum):
    DELIVERY = "delivery"
    RESCUE = "rescue"
    MEDICAL_RESPONSE = "medical_response"
    ASSESSMENT = "assessment"
    EVACUATION = "evacuation"
    SETUP = "setup"
    OTHER = "other"


class TaskStatus(str, Enum):
    AVAILABLE = "available"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskCreate(BaseModel):
    title: str
    description: str
    task_type: TaskType
    location: str
    priority: TaskPriority
    estimated_duration: Optional[int] = None  # minutes
    required_skills: Optional[List[str]] = []
    required_resources: Optional[Dict[str, int]] = {}  # resource_id: quantity
    request_id: Optional[str] = None


class TaskOut(BaseModel):
    id: str
    title: str
    description: str
    task_type: TaskType
    location: str
    priority: TaskPriority
    status: TaskStatus
    estimated_duration: Optional[int]
    required_skills: Optional[List[str]]
    required_resources: Optional[Dict[str, int]]
    assigned_to: Optional[str]
    assignee_name: Optional[str]
    request_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    completion_notes: Optional[str]


class TaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None
    assigned_to: Optional[str] = None
    priority: Optional[TaskPriority] = None
    completion_notes: Optional[str] = None


class TaskAccept(BaseModel):
    notes: Optional[str] = None


class TaskComplete(BaseModel):
    completion_notes: str
    resources_used: Optional[Dict[str, int]] = {}  # actual resources used


# SQLAlchemy Database Model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    task_type = Column(SQLEnum(TaskType), nullable=False, default=TaskType.OTHER)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.AVAILABLE)
    priority = Column(
        SQLEnum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM
    )
    assigned_to = Column(String, ForeignKey("users.id"), nullable=True)
    request_id = Column(String, ForeignKey("requests.id"), nullable=True)
    location = Column(String, nullable=True)
    estimated_duration = Column(Integer, nullable=True)  # minutes
    skills_required = Column(Text, nullable=True)  # JSON stored as text
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    def to_dict(self):
        """Convert to dictionary for API responses"""
        import json

        skills_list = []
        if self.skills_required:
            try:
                skills_list = json.loads(self.skills_required)
            except (json.JSONDecodeError, TypeError):
                skills_list = []

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "task_type": self.task_type.value if self.task_type else None,
            "status": self.status.value if self.status else None,
            "priority": self.priority.value if self.priority else None,
            "assigned_to": self.assigned_to,
            "request_id": self.request_id,
            "location": self.location,
            "estimated_duration": self.estimated_duration,
            "skills_required": skills_list,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
        }
