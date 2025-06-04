# ai_services/models/request.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, DateTime, Text, Enum as SQLEnum, ForeignKey
from core.database import Base
import uuid


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


# SQLAlchemy Database Model
class Request(Base):
    __tablename__ = "requests"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=True)
    contact_info = Column(String, nullable=True)
    reporter_id = Column(String, ForeignKey("users.id"), nullable=True)
    request_type = Column(
        SQLEnum(RequestType), nullable=True, default=RequestType.OTHER
    )
    priority = Column(SQLEnum(Priority), nullable=False, default=Priority.MEDIUM)
    status = Column(
        SQLEnum(RequestStatus), nullable=False, default=RequestStatus.PENDING
    )
    urgency_level = Column(String, nullable=True)
    needs = Column(Text, nullable=True)  # JSON stored as text
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_to = Column(String, ForeignKey("users.id"), nullable=True)

    def to_dict(self):
        """Convert to dictionary for API responses"""
        import json

        needs_list = []
        if self.needs:
            try:
                needs_list = json.loads(self.needs)
            except (json.JSONDecodeError, TypeError):
                needs_list = []

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "contact_info": self.contact_info,
            "reporter_id": self.reporter_id,
            "request_type": self.request_type.value if self.request_type else None,
            "priority": self.priority.value if self.priority else None,
            "status": self.status.value if self.status else None,
            "urgency_level": self.urgency_level,
            "needs": needs_list,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "assigned_to": self.assigned_to,
        }
