# ai_services/models/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Boolean, DateTime, Text, Enum as SQLEnum
from core.database import Base
import uuid
import json


class UserRole(str, Enum):
    AFFECTED = "affected"
    VOLUNTEER = "volunteer"
    FIRST_RESPONDER = "first_responder"
    ADMIN = "admin"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


# SQLAlchemy Database Model
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.AFFECTED)
    status = Column(SQLEnum(UserStatus), nullable=False, default=UserStatus.ACTIVE)
    location = Column(String, nullable=True)
    skills = Column(Text, nullable=True)  # JSON stored as text
    availability = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    def to_dict(self):
        """Convert to dictionary for API responses"""
        skills_list = []
        if self.skills:
            try:
                skills_list = json.loads(self.skills)
            except (json.JSONDecodeError, TypeError):
                skills_list = []

        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "phone": self.phone,
            "role": self.role.value if self.role else None,
            "status": self.status.value if self.status else None,
            "location": self.location,
            "skills": skills_list,
            "availability": self.availability,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }


# Pydantic Models for API
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    role: UserRole
    location: Optional[str] = None
    skills: Optional[List[str]] = []
    availability: Optional[bool] = True


class UserOut(BaseModel):
    id: str
    email: str
    full_name: str
    phone: Optional[str]
    role: UserRole
    status: UserStatus
    location: Optional[str]
    skills: Optional[List[str]]
    availability: Optional[bool]
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = None
    availability: Optional[bool] = None
    status: Optional[UserStatus] = None


class UserProfile(BaseModel):
    full_name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = []
    availability: Optional[bool] = True
