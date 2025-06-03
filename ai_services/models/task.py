# ai_services/models/task.py
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

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
