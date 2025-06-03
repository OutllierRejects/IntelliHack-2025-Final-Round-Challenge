# ai_services/models/resource.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ResourceType(str, Enum):
    FOOD = "food"
    WATER = "water"
    MEDICAL_SUPPLIES = "medical_supplies"
    EQUIPMENT = "equipment"
    VEHICLES = "vehicles"
    PERSONNEL = "personnel"
    TOOLS = "tools"
    OTHER = "other"


class ResourceUnit(str, Enum):
    PIECES = "pieces"
    LITERS = "liters"
    KILOGRAMS = "kilograms"
    BOXES = "boxes"
    UNITS = "units"
    PEOPLE = "people"


class ResourceCreate(BaseModel):
    name: str
    resource_type: ResourceType
    unit: ResourceUnit
    current_quantity: int
    minimum_threshold: int
    maximum_capacity: int
    location: Optional[str] = None
    description: Optional[str] = None


class ResourceOut(BaseModel):
    id: str
    name: str
    resource_type: ResourceType
    unit: ResourceUnit
    current_quantity: int
    minimum_threshold: int
    maximum_capacity: int
    location: Optional[str]
    description: Optional[str]
    is_low_stock: bool
    created_at: datetime
    updated_at: Optional[datetime]


class ResourceUpdate(BaseModel):
    current_quantity: Optional[int] = None
    minimum_threshold: Optional[int] = None
    maximum_capacity: Optional[int] = None
    location: Optional[str] = None


class ResourceReplenish(BaseModel):
    quantity: int
    notes: Optional[str] = None


class ResourceConsume(BaseModel):
    quantity: int
    task_id: Optional[str] = None
    notes: Optional[str] = None
