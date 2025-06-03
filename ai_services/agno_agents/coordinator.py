"""
AGNO Agent Coordinator - Orchestrates the multi-agent workflow for disaster response
Coordinates: Intake → Prioritization → Assignment → Communication
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import json

from .intake_agent import IntakeAgent
from .prioritization_agent import PrioritizationAgent  
from .assignment_agent import AssignmentAgent
from .communication_agent import CommunicationAgent
from core.database import get_supabase_client
from core.redis_client import get_redis_client

logger = logging.getLogger(__name__)

class AgentCoordinator:
    """
    Coordinates the AGNO agents workflow for disaster response processing
    """
    
    def __init__(self):
        """Initialize the agent coordinator with all agents"""
        self.supabase = get_supabase_client()
        self.redis = get_redis_client()
        
        # Initialize all agents
        self.intake_agent = IntakeAgent()
        self.prioritization_agent = PrioritizationAgent()
        self.assignment_agent = AssignmentAgent()
        self.communication_agent = CommunicationAgent()
        
        # Initialize agents dict
        self._initialize_agents()
        
        # Processing state
        self.is_processing = False
        self.last_processed_at = None
        self.processing_stats = {
            "total_processed": 0,
            "successful": 0,
            "failed": 0,
            "last_error": None
        }
    
    async def start_processing_loop(self, interval_seconds: int = 30):
        """
        Start the continuous processing loop for pending requests
        
        Args:
            interval_seconds: How often to check for new requests
        """
        logger.info(f"Starting AGNO agent coordinator with {interval_seconds}s interval")
        
        while True:
            try:
                await self.process_pending_requests()
                await asyncio.sleep(interval_seconds)
            except Exception as e:
                logger.error(f"Error in processing loop: {e}")
                self.processing_stats["last_error"] = str(e)
                await asyncio.sleep(interval_seconds)  # Continue despite errors
    
    async def process_pending_requests(self):
        """
        Process all pending disaster requests through the agent pipeline
        """
        if self.is_processing:
            logger.debug("Already processing requests, skipping...")
            return
        
        self.is_processing = True
        processed_count = 0
        
        try:
            # Step 1: Get new/pending requests from database
            pending_requests = await self._get_pending_requests()
            
            if not pending_requests:
                logger.debug("No pending requests to process")
                return
            
            logger.info(f"Processing {len(pending_requests)} pending requests")
            
            # Step 2: Process each request through the agent pipeline
            for request in pending_requests:
                try:
                    await self._process_single_request(request)
                    processed_count += 1
                    self.processing_stats["successful"] += 1
                except Exception as e:
                    logger.error(f"Failed to process request {request.get('id')}: {e}")
                    self.processing_stats["failed"] += 1
                    await self._mark_request_failed(request.get('id'), str(e))
            
            self.processing_stats["total_processed"] += processed_count
            self.last_processed_at = datetime.now(timezone.utc)
            
            logger.info(f"Successfully processed {processed_count} requests")
            
        except Exception as e:
            logger.error(f"Error in process_pending_requests: {e}")
            self.processing_stats["last_error"] = str(e)
        finally:
            self.is_processing = False
    
    async def _process_single_request(self, request: Dict[str, Any]):
        """
        Process a single request through the complete agent pipeline
        
        Args:
            request: The disaster request to process
        """
        request_id = request.get('id')
        logger.info(f"Starting agent pipeline for request {request_id}")
        
        try:
            # Step 1: Intake Agent - Process and validate the request
            logger.debug(f"Step 1: Intake processing for request {request_id}")
            intake_result = await self.intake_agent.process_request(request)
            
            if not intake_result.get('success'):
                raise Exception(f"Intake failed: {intake_result.get('error')}")
            
            await self._update_request_status(request_id, 'INTAKE_COMPLETE', intake_result)
            
            # Step 2: Prioritization Agent - Determine priority and urgency
            logger.debug(f"Step 2: Prioritization for request {request_id}")
            prioritization_result = await self.prioritization_agent.prioritize([intake_result])
            
            if not prioritization_result:
                raise Exception("Prioritization failed")
            
            priority_data = prioritization_result[0]  # Single request result
            await self._update_request_status(request_id, 'PRIORITIZED', priority_data)
            
            # Step 3: Assignment Agent - Assign resources and responders
            logger.debug(f"Step 3: Resource assignment for request {request_id}")
            available_resources = await self._get_available_resources()
            assignment_result = await self.assignment_agent.assign(priority_data, available_resources)
            
            if not assignment_result.get('assignments'):
                logger.warning(f"No resources could be assigned to request {request_id}")
                await self._update_request_status(request_id, 'NO_RESOURCES_AVAILABLE', assignment_result)
                return
            
            await self._update_request_status(request_id, 'RESOURCES_ASSIGNED', assignment_result)
            await self._create_resource_assignments(request_id, assignment_result['assignments'])
            
            # Step 4: Communication Agent - Generate and send notifications
            logger.debug(f"Step 4: Communication for request {request_id}")
            stakeholders = await self._get_request_stakeholders(request_id)
            
            incident_data = {
                **priority_data,
                **assignment_result,
                'id': request_id,
                'status': 'RESOURCES_ASSIGNED'
            }
            
            communication_result = await self.communication_agent.generate_notifications(
                incident_data, stakeholders
            )
            
            # Send notifications
            for notification in communication_result.get('notifications', []):
                await self.communication_agent.send_notification(notification)
            
            await self._update_request_status(request_id, 'PROCESSING_COMPLETE', communication_result)
            
            logger.info(f"Successfully completed agent pipeline for request {request_id}")
            
        except Exception as e:
            logger.error(f"Agent pipeline failed for request {request_id}: {e}")
            await self._mark_request_failed(request_id, str(e))
            raise
    
    async def _get_pending_requests(self) -> List[Dict[str, Any]]:
        """Get all pending disaster requests from the database"""
        try:
            response = (
                self.supabase
                .table('disaster_requests')
                .select('*')
                .in_('status', ['PENDING', 'SUBMITTED', 'RETRY'])
                .order('created_at', desc=False)
                .limit(50)  # Process in batches
                .execute()
            )
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching pending requests: {e}")
            return []
    
    async def _get_available_resources(self) -> List[Dict[str, Any]]:
        """Get all available resources from the database"""
        try:
            response = (
                self.supabase
                .table('resources')
                .select('*')
                .eq('status', 'AVAILABLE')
                .execute()
            )
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching available resources: {e}")
            return []
    
    async def _get_request_stakeholders(self, request_id: str) -> List[Dict[str, Any]]:
        """Get stakeholders for notifications"""
        stakeholders = []
        
        try:
            # Add the request reporter
            request_response = (
                self.supabase
                .table('disaster_requests')
                .select('reporter_contact, reporter_phone')
                .eq('id', request_id)
                .execute()
            )
            
            if request_response.data:
                request_data = request_response.data[0]
                if request_data.get('reporter_contact'):
                    stakeholders.append({
                        'type': 'REQUESTER',
                        'contact': request_data['reporter_contact'],
                        'phone': request_data.get('reporter_phone')
                    })
            
            # Add assigned responders
            assignments_response = (
                self.supabase
                .table('resource_assignments')
                .select('resources(*)')
                .eq('incident_id', request_id)
                .execute()
            )
            
            for assignment in assignments_response.data or []:
                resource = assignment.get('resources', {})
                if resource.get('assigned_to'):
                    stakeholders.append({
                        'type': 'RESPONDER',
                        'contact': resource['assigned_to']
                    })
            
            # Add volunteers in the area (optional)
            # This could be enhanced to find volunteers near the incident location
            
        except Exception as e:
            logger.error(f"Error fetching stakeholders for request {request_id}: {e}")
        
        return stakeholders
    
    async def _update_request_status(self, request_id: str, status: str, data: Dict[str, Any]):
        """Update request status and processing data"""
        try:
            update_data = {
                'status': status,
                'updated_at': datetime.now(timezone.utc).isoformat(),
                'agent_processing_data': data
            }
            
            self.supabase.table('disaster_requests').update(update_data).eq('id', request_id).execute()
            
            # Also cache in Redis for quick access
            await self.redis.setex(
                f"request_status:{request_id}",
                3600,  # 1 hour TTL
                json.dumps({'status': status, 'updated_at': update_data['updated_at']})
            )
            
        except Exception as e:
            logger.error(f"Error updating request status: {e}")
    
    async def _create_resource_assignments(self, request_id: str, assignments: List[Dict[str, Any]]):
        """Create resource assignment records"""
        try:
            assignment_records = []
            for assignment in assignments:
                assignment_records.append({
                    'resource_id': assignment['resource_id'],
                    'incident_id': request_id,
                    'assigned_at': datetime.now(timezone.utc).isoformat(),
                    'status': 'ASSIGNED',
                    'assignment_reasoning': assignment.get('reasoning', ''),
                    'estimated_arrival': assignment.get('estimated_arrival')
                })
            
            if assignment_records:
                self.supabase.table('resource_assignments').insert(assignment_records).execute()
                
                # Update resource status to ASSIGNED
                for assignment in assignments:
                    self.supabase.table('resources').update({
                        'status': 'ASSIGNED',
                        'current_incident_id': request_id
                    }).eq('id', assignment['resource_id']).execute()
                    
        except Exception as e:
            logger.error(f"Error creating resource assignments: {e}")
    
    async def _mark_request_failed(self, request_id: str, error_message: str):
        """Mark a request as failed with error details"""
        try:
            self.supabase.table('disaster_requests').update({
                'status': 'PROCESSING_FAILED',
                'error_message': error_message,
                'updated_at': datetime.now(timezone.utc).isoformat()
            }).eq('id', request_id).execute()
        except Exception as e:
            logger.error(f"Error marking request as failed: {e}")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get coordinator status and statistics"""
        return {
            'is_processing': self.is_processing,
            'last_processed_at': self.last_processed_at.isoformat() if self.last_processed_at else None,
            'statistics': self.processing_stats,
            'agents_status': {
                'intake_agent': 'active',
                'prioritization_agent': 'active', 
                'assignment_agent': 'active',
                'communication_agent': 'active'
            }
        }
    
    async def trigger_immediate_processing(self) -> Dict[str, Any]:
        """Trigger immediate processing of pending requests"""
        if self.is_processing:
            return {
                'status': 'already_processing',
                'message': 'Agent coordinator is already processing requests'
            }
        
        # Start processing in background
        asyncio.create_task(self.process_pending_requests())
        
        return {
            'status': 'processing_started',
            'message': 'Immediate processing triggered successfully'
        }

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        try:
            return {
                "status": "active" if self.agents else "inactive",
                "active_agents": [
                    agent.name for agent in self.agents.values() 
                    if hasattr(agent, 'name')
                ],
                "queue_size": 0,  # Could integrate with Redis queue
                "last_activity": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {"status": "error", "active_agents": [], "queue_size": 0}

    async def process_incidents_batch(
        self, 
        incident_ids: List[str], 
        priority_override: Optional[str] = None,
        processing_id: str = None
    ) -> Dict[str, Any]:
        """Process a batch of incidents"""
        try:
            logger.info(f"Processing batch of {len(incident_ids)} incidents")
            results = []
            
            for incident_id in incident_ids:
                try:
                    # Get incident data
                    incident_data = await self._get_incident_data(incident_id)
                    if not incident_data:
                        continue
                    
                    # Override priority if specified
                    if priority_override:
                        incident_data['priority'] = priority_override
                    
                    # Process through pipeline
                    result = await self.process_incident_pipeline(incident_data)
                    results.append(result)
                    
                except Exception as e:
                    logger.error(f"Failed to process incident {incident_id}: {e}")
                    results.append({
                        "incident_id": incident_id,
                        "success": False,
                        "error": str(e)
                    })
            
            return {
                "processing_id": processing_id,
                "completed": True,
                "results": results,
                "summary": {
                    "total": len(incident_ids),
                    "successful": len([r for r in results if r.get("success", False)]),
                    "failed": len([r for r in results if not r.get("success", False)])
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to process incident batch: {e}")
            return {
                "processing_id": processing_id,
                "completed": False,
                "error": str(e)
            }

    def restart_system(self) -> bool:
        """Restart the agent system"""
        try:
            logger.info("Restarting agent system...")
            
            # Re-initialize agents
            self._initialize_agents()
            
            logger.info("Agent system restarted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restart agent system: {e}")
            return False

    def get_processing_status(self, processing_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a processing job"""
        try:
            # This could be enhanced with Redis to store processing status
            # For now, return a simple response
            return {
                "processing_id": processing_id,
                "completed": True,
                "message": "Processing completed",
                "results": {"status": "simulated"}
            }
        except Exception as e:
            logger.error(f"Failed to get processing status: {e}")
            return None

    async def process_new_incidents(self, processing_id: str = None) -> Dict[str, Any]:
        """Process all new incidents"""
        try:
            # Get new incidents from database
            supabase = get_supabase_client()
            response = supabase.table("requests").select("*").eq("status", "pending").execute()
            
            if not response.data:
                return {
                    "processing_id": processing_id,
                    "completed": True,
                    "message": "No new incidents to process",
                    "results": []
                }
            
            # Process each incident
            incident_ids = [str(incident["id"]) for incident in response.data]
            return await self.process_incidents_batch(incident_ids, processing_id=processing_id)
            
        except Exception as e:
            logger.error(f"Failed to process new incidents: {e}")
            return {
                "processing_id": processing_id,
                "completed": False,
                "error": str(e)
            }

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        try:
            return {
                "total_agents": len(self.agents),
                "active_agents": len([a for a in self.agents.values() if a]),
                "uptime": "N/A",  # Could track actual uptime
                "processing_stats": {
                    "total_processed": 0,  # Could track in Redis
                    "success_rate": 0.0,
                    "average_response_time": 0.0
                }
            }
        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return {}

    def _initialize_agents(self):
        """Initialize or re-initialize all agents"""
        try:
            self.agents = {
                "intake": self.intake_agent,
                "prioritization": self.prioritization_agent,
                "assignment": self.assignment_agent,
                "communication": self.communication_agent
            }
            logger.info("Agents initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize agents: {e}")
            self.agents = {}

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        try:
            return {
                "status": "active" if hasattr(self, 'agents') and self.agents else "inactive",
                "active_agents": list(self.agents.keys()) if hasattr(self, 'agents') else [],
                "queue_size": 0,  # Could integrate with Redis queue
                "last_activity": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {"status": "error", "active_agents": [], "queue_size": 0}

    async def process_incidents_batch(
        self, 
        incident_ids: List[str], 
        priority_override: Optional[str] = None,
        processing_id: str = None
    ) -> Dict[str, Any]:
        """Process a batch of incidents"""
        try:
            logger.info(f"Processing batch of {len(incident_ids)} incidents")
            results = []
            
            for incident_id in incident_ids:
                try:
                    # Get incident data
                    incident_data = await self._get_incident_data(incident_id)
                    if not incident_data:
                        continue
                    
                    # Override priority if specified
                    if priority_override:
                        incident_data['priority'] = priority_override
                    
                    # Process through pipeline
                    result = await self.process_incident_pipeline(incident_data)
                    results.append(result)
                    
                except Exception as e:
                    logger.error(f"Failed to process incident {incident_id}: {e}")
                    results.append({
                        "incident_id": incident_id,
                        "success": False,
                        "error": str(e)
                    })
            
            return {
                "processing_id": processing_id,
                "completed": True,
                "results": results,
                "summary": {
                    "total": len(incident_ids),
                    "successful": len([r for r in results if r.get("success", False)]),
                    "failed": len([r for r in results if not r.get("success", False)])
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to process incident batch: {e}")
            return {
                "processing_id": processing_id,
                "completed": False,
                "error": str(e)
            }

    async def process_incident_pipeline(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single incident through the pipeline"""
        try:
            return {
                "incident_id": incident_data.get("id"),
                "success": True,
                "message": "Processed successfully (simulated)",
                "pipeline_stages": ["intake", "prioritization", "assignment", "communication"]
            }
        except Exception as e:
            logger.error(f"Pipeline processing failed: {e}")
            return {
                "incident_id": incident_data.get("id"),
                "success": False,
                "error": str(e)
            }

    def restart_system(self) -> bool:
        """Restart the agent system"""
        try:
            logger.info("Restarting agent system...")
            
            # Re-initialize agents
            self._initialize_agents()
            
            logger.info("Agent system restarted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restart agent system: {e}")
            return False

    def get_processing_status(self, processing_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a processing job"""
        try:
            # This could be enhanced with Redis to store processing status
            # For now, return a simple response
            return {
                "processing_id": processing_id,
                "completed": True,
                "message": "Processing completed",
                "results": {"status": "simulated"}
            }
        except Exception as e:
            logger.error(f"Failed to get processing status: {e}")
            return None

    async def process_new_incidents(self, processing_id: str = None) -> Dict[str, Any]:
        """Process all new incidents"""
        try:
            # Get new incidents from database
            response = self.supabase.table("requests").select("*").eq("status", "pending").execute()
            
            if not response.data:
                return {
                    "processing_id": processing_id,
                    "completed": True,
                    "message": "No new incidents to process",
                    "results": []
                }
            
            # Process each incident
            incident_ids = [str(incident["id"]) for incident in response.data]
            return await self.process_incidents_batch(incident_ids, processing_id=processing_id)
            
        except Exception as e:
            logger.error(f"Failed to process new incidents: {e}")
            return {
                "processing_id": processing_id,
                "completed": False,
                "error": str(e)
            }

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        try:
            return {
                "total_agents": len(getattr(self, 'agents', {})),
                "active_agents": len([a for a in getattr(self, 'agents', {}).values() if a]),
                "uptime": "N/A",  # Could track actual uptime
                "processing_stats": {
                    "total_processed": self.processing_stats.get("total_processed", 0),
                    "success_rate": 0.0,
                    "average_response_time": 0.0
                }
            }
        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return {}

    async def _get_incident_data(self, incident_id: str) -> Optional[Dict[str, Any]]:
        """Get incident data from database"""
        try:
            response = self.supabase.table("requests").select("*").eq("id", incident_id).execute()
            
            if response.data:
                return response.data[0]
            return None
            
        except Exception as e:
            logger.error(f"Failed to get incident data: {e}")
            return None
```
