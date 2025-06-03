# ai_services/models/request.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RequestType(str, Enum):
    FOOD = "food"
    WATER = "water"
    MEDICAL = "medical"
    SHELTER = "shelter"
    RESCUE = "rescue"
    OTHER = "other"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RequestStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RequestCreate(BaseModel):
    title: str
    description: str
    location: Optional[str] = None
    contact_info: Optional[str] = None
    urgency_level: Optional[str] = None
    needs: Optional[List[str]] = []


class RequestOut(BaseModel):
    id: str
    title: str
    description: str
    location: Optional[str]
    contact_info: Optional[str]
    reporter_id: Optional[str]
    request_type: Optional[RequestType]
    priority: Optional[Priority]
    status: RequestStatus
    needs: Optional[List[str]]
    created_at: datetime
    updated_at: Optional[datetime]
    assigned_to: Optional[str]


class RequestUpdate(BaseModel):
    priority: Optional[Priority] = None
    status: Optional[RequestStatus] = None
    assigned_to: Optional[str] = None
    notes: Optional[str] = None
