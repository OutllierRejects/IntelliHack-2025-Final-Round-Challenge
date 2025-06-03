# ai_services/api/endpoints/resources.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from models.resource import ResourceCreate, ResourceOut, ResourceUpdate
from services.resource_service import (
    get_resources, replenish_resource, create_resource,
    get_low_stock_resources, get_resource_dashboard_stats
)
from core.auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/resources", response_model=List[ResourceOut])
def get_resource_list(
    user=Depends(get_current_user),
    resource_type: Optional[str] = None,
    location: Optional[str] = None,
    low_stock: bool = False
):
    """Get resources with optional filtering"""
    try:
        filters = {}
        if resource_type:
            filters["resource_type"] = resource_type
        if location:
            filters["location"] = location
        if low_stock:
            filters["low_stock"] = True
        
        return get_resources(filters)
    except Exception as e:
        logger.error(f"Failed to get resources: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources/low-stock", response_model=List[ResourceOut])
def get_low_stock_resource_list(user=Depends(get_current_user)):
    """Get resources that are below their threshold"""
    try:
        return get_low_stock_resources()
    except Exception as e:
        logger.error(f"Failed to get low stock resources: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/resources", response_model=ResourceOut)
def create_new_resource(
    payload: ResourceCreate,
    user=Depends(get_current_user)
):
    """Create a new resource (admin only)"""
    try:
        user_role = user.get("role", "volunteer")
        if user_role != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
        
        resource_data = payload.model_dump()
        resource_data["created_by"] = user.get("id") or user.get("email")
        
        return create_resource(resource_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create resource: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/resources/{resource_id}/replenish", response_model=ResourceOut)
def replenish_resource_stock(
    resource_id: str,
    amount: int,
    user=Depends(get_current_user)
):
    """Replenish resource stock (admin only)"""
    try:
        user_role = user.get("role", "volunteer")
        if user_role != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
        
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        
        result = replenish_resource(resource_id, amount)
        if not result:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to replenish resource {resource_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources/dashboard/stats")
def get_resource_dashboard_stats_endpoint(user=Depends(get_current_user)):
    """Get resource dashboard statistics"""
    try:
        user_role = user.get("role", "volunteer")
        if user_role not in ["admin", "first_responder"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        return get_resource_dashboard_stats()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get resource dashboard stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
