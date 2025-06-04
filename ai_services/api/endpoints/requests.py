# ai_services/api/endpoints/requests.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from models.request import RequestCreate, RequestOut, RequestUpdate
from services.request_service import create_request, get_requests, update_request_status
from core.auth import get_current_user
from agno_agents.intake_agent import process_intake
from agno_agents.prioritization_agent import prioritize_request
from typing import List, Optional

router = APIRouter()

@router.post("/requests", response_model=RequestOut)
def submit_help_request(
    payload: RequestCreate,
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user)
):
    """Submit a new help request - triggers AI processing pipeline"""
    try:
        # Add user info to request
        request_data = payload.model_dump()
        request_data["requester_id"] = user.get("id") or user.get("email")
        
        # Create request in database
        new_request = create_request(request_data)
        
        # Trigger AI processing pipeline in background
        background_tasks.add_task(process_request_with_ai, new_request["id"], request_data)
        
        return new_request
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/requests", response_model=List[RequestOut])
def get_help_requests(
    user=Depends(get_current_user),
    status: Optional[str] = None,
    priority: Optional[str] = None,
    request_type: Optional[str] = None,
    limit: int = 50
):
    """Get help requests with optional filtering"""
    try:
        filters = {}
        if status:
            filters["status"] = status
        if priority:
            filters["priority"] = priority
        if request_type:
            filters["request_type"] = request_type
            
        # Role-based access control
        user_role = user.get("role", "affected")
        if user_role == "affected":
            filters["requester_id"] = user.get("id") or user.get("email")
        
        return get_requests(filters, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/requests/{request_id}", response_model=RequestOut)
def get_request_details(request_id: str, user=Depends(get_current_user)):
    """Get specific request details"""
    try:
        requests = get_requests({"id": request_id}, 1)
        if not requests:
            raise HTTPException(status_code=404, detail="Request not found")
        
        request = requests[0]
        
        # Check access permissions
        user_role = user.get("role", "affected")
        user_id = user.get("id") or user.get("email")
        
        if user_role == "affected" and request.get("requester_id") != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return request
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/requests/{request_id}", response_model=RequestOut)
def update_help_request(
    request_id: str,
    payload: RequestUpdate,
    user=Depends(get_current_user)
):
    """Update request status or priority (admin/responder only)"""
    try:
        user_role = user.get("role", "affected")
        if user_role not in ["admin", "responder"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        update_data = payload.model_dump(exclude_unset=True)
        update_data["updated_by"] = user.get("id") or user.get("email")
        
        updated_request = update_request_status(request_id, update_data)
        if not updated_request:
            raise HTTPException(status_code=404, detail="Request not found")
        
        return updated_request
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/requests/dashboard/stats")
def get_dashboard_stats(user=Depends(get_current_user)):
    """Get dashboard statistics"""
    try:
        from core.database import supabase
        
        # Get counts by status
        status_counts = {}
        for status in ["pending", "processing", "assigned", "completed"]:
            response = supabase.table("requests").select("id").eq("status", status).execute()
            status_counts[status] = len(response.data)
        
        # Get counts by priority
        priority_counts = {}
        for priority in ["critical", "high", "medium", "low"]:
            response = supabase.table("requests").select("id").eq("priority", priority).execute()
            priority_counts[priority] = len(response.data)
        
        # Get recent requests
        recent_response = supabase.table("requests").select("*").order("created_at", desc=True).limit(10).execute()
        recent_requests = recent_response.data
        
        return {
            "status_counts": status_counts,
            "priority_counts": priority_counts,
            "recent_requests": recent_requests,
            "total_requests": sum(status_counts.values())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def process_request_with_ai(request_id: str, request_data: dict):
    """Background task to process request through AI pipeline"""
    try:
        # Step 1: Intake processing
        intake_result = process_intake(request_id, request_data)
        
        # Step 2: Prioritization
        if intake_result.get("db_updated"):
            priority_result = prioritize_request(request_id, intake_result)
            
        logger.info(f"AI processing completed for request {request_id}")
    except Exception as e:
        logger.error(f"AI processing failed for request {request_id}: {e}")
