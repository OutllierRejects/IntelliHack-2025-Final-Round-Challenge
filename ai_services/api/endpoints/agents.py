# ai_services/api/endpoints/agents.py
"""
AGNO Agent endpoints for disaster response coordination
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, List, Optional
from pydantic import BaseModel
from agno_agents.coordinator import AgentCoordinator
from core.auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize agent coordinator
try:
    agent_coordinator = AgentCoordinator()
except Exception as e:
    logger.error(f"Failed to initialize agent coordinator: {e}")
    agent_coordinator = None


class AgentProcessRequest(BaseModel):
    """Request to process incidents through agent pipeline"""

    incident_ids: List[str]
    priority_override: Optional[str] = None


class AgentStatus(BaseModel):
    """Agent system status"""

    status: str
    active_agents: List[str]
    processing_queue: int
    last_activity: Optional[str]


class AgentResponse(BaseModel):
    """Agent processing response"""

    success: bool
    message: str
    processing_id: Optional[str] = None
    results: Optional[Dict] = None


@router.get("/agents/status", response_model=AgentStatus)
def get_agent_status(user=Depends(get_current_user)) -> AgentStatus:
    """Get current status of AGNO agent system"""
    try:
        if not agent_coordinator:
            return AgentStatus(
                status="error", active_agents=[], processing_queue=0, last_activity=None
            )

        status_info = agent_coordinator.get_system_status()

        return AgentStatus(
            status=status_info.get("status", "unknown"),
            active_agents=status_info.get("active_agents", []),
            processing_queue=status_info.get("queue_size", 0),
            last_activity=status_info.get("last_activity"),
        )

    except Exception as e:
        logger.error(f"Failed to get agent status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/process", response_model=AgentResponse)
def process_incidents_with_agents(
    request: AgentProcessRequest,
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user),
) -> AgentResponse:
    """Process incidents through AGNO agent pipeline"""
    try:
        if not agent_coordinator:
            raise HTTPException(
                status_code=503, detail="Agent coordinator not available"
            )

        user_role = user.get("role", "volunteer")
        if user_role not in ["admin", "first_responder"]:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions to trigger agent processing",
            )

        if not request.incident_ids:
            raise HTTPException(
                status_code=400, detail="At least one incident ID is required"
            )

        # Start agent processing in background
        processing_id = f"proc_{user.get('id', 'unknown')}_{len(request.incident_ids)}"

        background_tasks.add_task(
            agent_coordinator.process_incidents_batch,
            request.incident_ids,
            priority_override=request.priority_override,
            processing_id=processing_id,
        )

        return AgentResponse(
            success=True,
            message=f"Started processing {len(request.incident_ids)} incidents",
            processing_id=processing_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to process incidents with agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/restart", response_model=AgentResponse)
def restart_agent_system(user=Depends(get_current_user)) -> AgentResponse:
    """Restart the AGNO agent system"""
    try:
        user_role = user.get("role", "volunteer")
        if user_role != "admin":
            raise HTTPException(
                status_code=403, detail="Admin access required to restart agents"
            )

        if not agent_coordinator:
            raise HTTPException(
                status_code=503, detail="Agent coordinator not available"
            )

        # Restart the agent system
        success = agent_coordinator.restart_system()

        if success:
            return AgentResponse(
                success=True, message="Agent system restarted successfully"
            )
        else:
            return AgentResponse(
                success=False, message="Failed to restart agent system"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to restart agent system: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/processing/{processing_id}", response_model=AgentResponse)
def get_processing_status(
    processing_id: str, user=Depends(get_current_user)
) -> AgentResponse:
    """Get status of a specific agent processing job"""
    try:
        if not agent_coordinator:
            raise HTTPException(
                status_code=503, detail="Agent coordinator not available"
            )

        status = agent_coordinator.get_processing_status(processing_id)

        if not status:
            raise HTTPException(status_code=404, detail="Processing job not found")

        return AgentResponse(
            success=status.get("completed", False),
            message=status.get("message", "Processing in progress"),
            processing_id=processing_id,
            results=status.get("results"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get processing status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/process-new", response_model=AgentResponse)
def process_new_incidents(
    background_tasks: BackgroundTasks, user=Depends(get_current_user)
) -> AgentResponse:
    """Process all new incidents through agent pipeline"""
    try:
        if not agent_coordinator:
            raise HTTPException(
                status_code=503, detail="Agent coordinator not available"
            )

        user_role = user.get("role", "volunteer")
        if user_role not in ["admin", "first_responder"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        # Start processing new incidents in background
        processing_id = f"new_proc_{user.get('id', 'unknown')}"

        background_tasks.add_task(
            agent_coordinator.process_new_incidents, processing_id=processing_id
        )

        return AgentResponse(
            success=True,
            message="Started processing new incidents",
            processing_id=processing_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to process new incidents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/metrics")
def get_agent_metrics(user=Depends(get_current_user)) -> Dict:
    """Get agent performance metrics"""
    try:
        user_role = user.get("role", "volunteer")
        if user_role not in ["admin", "first_responder"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        if not agent_coordinator:
            return {"status": "unavailable", "metrics": {}}

        metrics = agent_coordinator.get_performance_metrics()

        return {"status": "available", "metrics": metrics}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get agent metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
