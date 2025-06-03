# ai_services/models/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    AFFECTED = "affected"
    VOLUNTEER = "volunteer"
    FIRST_RESPONDER = "first_responder"
    ADMIN = "admin"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

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
