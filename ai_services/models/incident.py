# ai_services/models/incident.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class IncidentCreate(BaseModel):
    title: str
    description: str
    location: Optional[str] = None
    # reported_by: Optional[str] = None  # Could be user_id or email


class IncidentOut(BaseModel):
    id: str
    title: str
    description: str
    location: Optional[str]
    reported_by: Optional[str]
    created_at: datetime
