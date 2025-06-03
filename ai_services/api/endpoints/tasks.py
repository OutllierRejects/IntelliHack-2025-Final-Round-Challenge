# ai_services/api/endpoints/tasks.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Optional
from models.task import TaskCreate, TaskOut, TaskUpdate
from services.task_service import (
    create_task,
    get_tasks,
    update_task,
    assign_task,
    complete_task,
    get_available_tasks,
    get_user_tasks,
)
from core.auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/tasks", response_model=List[TaskOut])
def get_task_list(
    user=Depends(get_current_user),
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to_me: bool = False,
    limit: int = 50,
):
    """Get tasks with optional filtering"""
    try:
        filters = {}
        if status:
            filters["status"] = status
        if priority:
            filters["priority"] = priority

        user_role = user.get("role", "volunteer")
        user_id = user.get("id") or user.get("email")

        if assigned_to_me or user_role == "affected":
            # Show only user's tasks for affected individuals
            return get_user_tasks(user_id)
        elif user_role == "volunteer":
            # Show available tasks for volunteers
            if status == "open":
                return get_available_tasks("volunteer")
            else:
                filters["assignee_id"] = user_id
                return get_tasks(filters, limit)
        else:
            # Admins and responders see all tasks
            return get_tasks(filters, limit)

    except Exception as e:
        logger.error(f"Failed to get tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/available", response_model=List[TaskOut])
def get_available_task_list(
    user=Depends(get_current_user), location: Optional[str] = None
):
    """Get available tasks for assignment"""
    try:
        user_role = user.get("role", "volunteer")
        return get_available_tasks(user_role, location)
    except Exception as e:
        logger.error(f"Failed to get available tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/my-tasks", response_model=List[TaskOut])
def get_my_tasks(user=Depends(get_current_user)):
    """Get tasks assigned to the current user"""
    try:
        user_id = user.get("id") or user.get("email")
        return get_user_tasks(user_id)
    except Exception as e:
        logger.error(f"Failed to get user tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks", response_model=TaskOut)
def create_new_task(payload: TaskCreate, user=Depends(get_current_user)):
    """Create a new task (admin/responder only)"""
    try:
        user_role = user.get("role", "volunteer")
        if user_role not in ["admin", "first_responder"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        task_data = payload.model_dump()
        task_data["created_by"] = user.get("id") or user.get("email")

        return create_task(task_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/tasks/{task_id}/assign", response_model=TaskOut)
def assign_task_to_user(task_id: str, assignee_id: str, user=Depends(get_current_user)):
    """Assign a task to a user"""
    try:
        user_role = user.get("role", "volunteer")
        user_id = user.get("id") or user.get("email")

        # Volunteers can self-assign, others need admin/responder role
        if assignee_id != user_id and user_role not in ["admin", "first_responder"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        result = assign_task(task_id, assignee_id, user_id)
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to assign task {task_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/tasks/{task_id}/accept", response_model=TaskOut)
def accept_task(task_id: str, user=Depends(get_current_user)):
    """Accept a task (volunteer self-assignment)"""
    try:
        user_id = user.get("id") or user.get("email")
        result = assign_task(task_id, user_id, user_id)
        if not result:
            raise HTTPException(
                status_code=404, detail="Task not found or already assigned"
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to accept task {task_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/tasks/{task_id}/complete", response_model=TaskOut)
def complete_task_endpoint(
    task_id: str, completion_data: Optional[dict] = None, user=Depends(get_current_user)
):
    """Mark a task as completed"""
    try:
        user_id = user.get("id") or user.get("email")

        # Add completion info
        completion_info = completion_data or {}
        completion_info["completed_by"] = user_id

        result = complete_task(task_id, completion_info)
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to complete task {task_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task_endpoint(
    task_id: str, payload: TaskUpdate, user=Depends(get_current_user)
):
    """Update task details (admin/responder only)"""
    try:
        user_role = user.get("role", "volunteer")
        if user_role not in ["admin", "first_responder"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        update_data = payload.model_dump(exclude_unset=True)
        update_data["updated_by"] = user.get("id") or user.get("email")

        result = update_task(task_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update task {task_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/dashboard/stats")
def get_task_dashboard_stats(user=Depends(get_current_user)):
    """Get task dashboard statistics"""
    try:
        from services.task_service import get_tasks

        # Get counts by status
        status_counts = {}
        for status in ["open", "assigned", "in_progress", "completed"]:
            tasks = get_tasks({"status": status})
            status_counts[status] = len(tasks)

        # Get counts by priority
        priority_counts = {}
        for priority in ["critical", "high", "medium", "low"]:
            tasks = get_tasks({"priority": priority})
            priority_counts[priority] = len(tasks)

        # Get user's tasks if applicable
        user_id = user.get("id") or user.get("email")
        user_tasks = get_user_tasks(user_id)

        return {
            "status_counts": status_counts,
            "priority_counts": priority_counts,
            "user_task_count": len(user_tasks),
            "total_tasks": sum(status_counts.values()),
        }
    except Exception as e:
        logger.error(f"Failed to get task dashboard stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
