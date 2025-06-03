# ai_services/services/request_service.py
from typing import Dict, List, Optional
from datetime import datetime
from core.database import supabase
import logging

logger = logging.getLogger(__name__)


def create_request(request_data: Dict) -> Dict:
    """Create a new help request"""
    try:
        # Add timestamps
        now = datetime.utcnow().isoformat()
        request_data.update({
            "created_at": now,
            "updated_at": now,
            "status": "pending"
        })
        
        response = supabase.table("requests").insert(request_data).execute()
        
        if response.data:
            logger.info(f"Created new request: {response.data[0]['id']}")
            return response.data[0]
        else:
            raise Exception("Failed to create request - no data returned")
            
    except Exception as e:
        logger.error(f"Failed to create request: {e}")
        raise


def get_requests(filters: Dict = None, limit: int = 50) -> List[Dict]:
    """Get requests with optional filtering"""
    try:
        query = supabase.table("requests").select("*")
        
        if filters:
            for key, value in filters.items():
                if key == "id":
                    query = query.eq(key, value)
                elif key in ["status", "priority", "request_type", "requester_id"]:
                    query = query.eq(key, value)
                elif key == "urgency_level":
                    query = query.eq(key, value)
        
        response = query.order("created_at", desc=True).limit(limit).execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        logger.error(f"Failed to get requests: {e}")
        return []


def update_request_status(request_id: str, update_data: Dict) -> Optional[Dict]:
    """Update request status and other fields"""
    try:
        # Add updated timestamp
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        response = (
            supabase.table("requests")
            .update(update_data)
            .eq("id", request_id)
            .execute()
        )
        
        if response.data:
            logger.info(f"Updated request {request_id}")
            return response.data[0]
        else:
            logger.warning(f"No request found with id {request_id}")
            return None
            
    except Exception as e:
        logger.error(f"Failed to update request {request_id}: {e}")
        return None


def get_request_by_id(request_id: str) -> Optional[Dict]:
    """Get a specific request by ID"""
    try:
        response = (
            supabase.table("requests")
            .select("*")
            .eq("id", request_id)
            .execute()
        )
        
        if response.data:
            return response.data[0]
        else:
            return None
            
    except Exception as e:
        logger.error(f"Failed to get request {request_id}: {e}")
        return None


def get_dashboard_stats() -> Dict:
    """Get dashboard statistics for requests"""
    try:
        stats = {}
        
        # Get counts by status
        for status in ["pending", "processing", "assigned", "completed"]:
            response = supabase.table("requests").select("id").eq("status", status).execute()
            stats[f"{status}_count"] = len(response.data) if response.data else 0
        
        # Get counts by priority
        for priority in ["critical", "high", "medium", "low"]:
            response = supabase.table("requests").select("id").eq("priority", priority).execute()
            stats[f"{priority}_priority_count"] = len(response.data) if response.data else 0
        
        # Get total count
        response = supabase.table("requests").select("id").execute()
        stats["total_requests"] = len(response.data) if response.data else 0
        
        return stats
        
    except Exception as e:
        logger.error(f"Failed to get dashboard stats: {e}")
        return {}
