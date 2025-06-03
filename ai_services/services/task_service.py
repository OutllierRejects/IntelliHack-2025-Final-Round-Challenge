# ai_services/services/task_service.py
from typing import Dict, List, Optional
from datetime import datetime
from core.database import supabase
import logging

logger = logging.getLogger(__name__)


def create_task(task_data: Dict) -> Dict:
    """Create a new task"""
    try:
        # Add timestamps
        now = datetime.utcnow().isoformat()
        task_data.update({"created_at": now, "updated_at": now, "status": "open"})

        response = supabase.table("tasks").insert(task_data).execute()

        if response.data:
            logger.info(f"Created new task: {response.data[0]['id']}")
            return response.data[0]
        else:
            raise Exception("Failed to create task - no data returned")

    except Exception as e:
        logger.error(f"Failed to create task: {e}")
        raise


def get_tasks(filters: Dict = None, limit: int = 50) -> List[Dict]:
    """Get tasks with optional filtering"""
    try:
        query = supabase.table("tasks").select("*, requests(*), users(*)")

        if filters:
            for key, value in filters.items():
                if key == "id":
                    query = query.eq(key, value)
                elif key in [
                    "status",
                    "priority",
                    "task_type",
                    "assignee_id",
                    "request_id",
                ]:
                    query = query.eq(key, value)
                elif key == "assigned_to":
                    query = query.eq("assignee_id", value)

        response = query.order("created_at", desc=True).limit(limit).execute()

        return response.data if response.data else []

    except Exception as e:
        logger.error(f"Failed to get tasks: {e}")
        return []


def update_task(task_id: str, update_data: Dict) -> Optional[Dict]:
    """Update task data"""
    try:
        # Add updated timestamp
        update_data["updated_at"] = datetime.utcnow().isoformat()

        response = (
            supabase.table("tasks").update(update_data).eq("id", task_id).execute()
        )

        if response.data:
            logger.info(f"Updated task {task_id}")
            return response.data[0]
        else:
            logger.warning(f"No task found with id {task_id}")
            return None

    except Exception as e:
        logger.error(f"Failed to update task {task_id}: {e}")
        return None


def assign_task(
    task_id: str, assignee_id: str, assigned_by: str = None
) -> Optional[Dict]:
    """Assign a task to a user"""
    try:
        update_data = {
            "assignee_id": assignee_id,
            "status": "assigned",
            "assigned_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        if assigned_by:
            update_data["assigned_by"] = assigned_by

        response = (
            supabase.table("tasks").update(update_data).eq("id", task_id).execute()
        )

        if response.data:
            logger.info(f"Assigned task {task_id} to {assignee_id}")
            return response.data[0]
        else:
            return None

    except Exception as e:
        logger.error(f"Failed to assign task {task_id}: {e}")
        return None


def complete_task(task_id: str, completion_data: Dict = None) -> Optional[Dict]:
    """Mark a task as completed"""
    try:
        update_data = {
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        if completion_data:
            update_data.update(completion_data)

        response = (
            supabase.table("tasks").update(update_data).eq("id", task_id).execute()
        )

        if response.data:
            logger.info(f"Completed task {task_id}")
            return response.data[0]
        else:
            return None

    except Exception as e:
        logger.error(f"Failed to complete task {task_id}: {e}")
        return None


def get_available_tasks(user_role: str = None, location: str = None) -> List[Dict]:
    """Get available tasks for assignment"""
    try:
        query = supabase.table("tasks").select("*, requests(*)").eq("status", "open")

        if user_role == "volunteer":
            # Volunteers can only see non-critical tasks
            query = query.in_("priority", ["medium", "low"])

        response = (
            query.order("priority", desc=True).order("created_at", desc=False).execute()
        )

        return response.data if response.data else []

    except Exception as e:
        logger.error(f"Failed to get available tasks: {e}")
        return []


def get_user_tasks(user_id: str) -> List[Dict]:
    """Get tasks assigned to a specific user"""
    try:
        response = (
            supabase.table("tasks")
            .select("*, requests(*)")
            .eq("assignee_id", user_id)
            .in_("status", ["assigned", "in_progress"])
            .order("created_at", desc=True)
            .execute()
        )

        return response.data if response.data else []

    except Exception as e:
        logger.error(f"Failed to get user tasks for {user_id}: {e}")
        return []
