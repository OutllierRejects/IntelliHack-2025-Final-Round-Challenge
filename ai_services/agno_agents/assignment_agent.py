# ai_services/agno_agents/assignment_agent.py
import os
import logging
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from typing import Dict, List, Optional
from datetime import datetime
from core.database import supabase

logger = logging.getLogger(__name__)


class AssignmentAgent(Agent):
    """AGNO Agent for assigning tasks to volunteers and responders"""

    def __init__(self):
        # Initialize AGNO Agent with OpenAI only
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is required for AssignmentAgent")
        
        model = OpenAIChat(
            id="gpt-4o-mini",
            temperature=0.3,
            max_tokens=1200
        )
        
        super().__init__(
            name="DisasterAssignmentAgent",
            model=model,
            description="AI agent for intelligently assigning disaster response tasks to appropriate personnel",
            instructions="""
You are a disaster response assignment agent. Your job is to:
1. Match prioritized requests with available volunteers and responders
2. Consider personnel skills, location, and availability
3. Optimize resource allocation and response times
4. Create detailed task assignments with clear instructions
5. Reserve necessary resources for each assignment

Assignment criteria:
- CRITICAL/HIGH priority requests get first responders
- Match skills to needs (medical -> medics, rescue -> rescue teams)
- Minimize travel time when possible
- Balance workload across available personnel
- Ensure resource availability before assignment
- Create clear, actionable task instructions

Always prioritize life-safety assignments and ensure proper resource allocation.
""",
            add_history_to_messages=True,
            num_history_responses=5,
            markdown=False
        )
        self.version = "1.0.0"

    def get_prioritized_requests(self) -> List[Dict]:
        """Get prioritized requests ready for assignment"""
        try:
            response = (
                supabase.table("requests")
                .select("*")
                .eq("status", "prioritized")
                .order("priority_score", desc=True)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Failed to fetch prioritized requests: {e}")
            return []

    def get_available_personnel(self) -> List[Dict]:
        """Get available volunteers and responders"""
        try:
            # Get users with volunteer or responder roles who are available
            response = (
                supabase.table("users")
                .select("*")
                .in_("role", ["volunteer", "first_responder"])
                .eq("status", "available")
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Failed to fetch available personnel: {e}")
            return []

    def get_available_resources(self) -> Dict:
        """Get current resource availability"""
        try:
            response = (
                supabase.table("resources")
                .select("*")
                .gt("current_stock", 0)
                .execute()
            )
            resources = response.data if response.data else []
            
            # Organize by type and location
            availability = {}
            for resource in resources:
                res_type = resource.get("type", "unknown")
                location = resource.get("location", "unknown")
                key = f"{res_type}_{location}"
                
                availability[key] = {
                    "id": resource.get("id"),
                    "type": res_type,
                    "location": location,
                    "current_stock": resource.get("current_stock", 0),
                    "unit": resource.get("unit", "units"),
                    "description": resource.get("description", "")
                }
            
            return availability
        except Exception as e:
            logger.error(f"Failed to fetch available resources: {e}")
            return {}

    def create_assignments(self, requests: List[Dict], personnel: List[Dict], resources: Dict) -> List[Dict]:
        """Create task assignments using AI"""
        if not requests or not personnel:
            return []

        try:
            # Prepare data for AI
            requests_text = ""
            for i, req in enumerate(requests):
                requests_text += f"""
Request {i+1}:
- ID: {req.get('id')}
- Priority: {req.get('priority')} (Score: {req.get('priority_score', 0)})
- Type: {req.get('request_type')}
- Needs: {req.get('needs', [])}
- Location: {req.get('location', 'unknown')}
- Description: {req.get('description', '')}
- Special Requirements: {req.get('special_requirements', '')}
- Recommended Action: {req.get('recommended_action', '')}
"""

            personnel_text = ""
            for i, person in enumerate(personnel):
                personnel_text += f"""
Person {i+1}:
- ID: {person.get('id')}
- Name: {person.get('name', 'Unknown')}
- Role: {person.get('role')}
- Skills: {person.get('skills', [])}
- Location: {person.get('location', 'unknown')}
- Max Tasks: {person.get('max_concurrent_tasks', 3)}
- Current Tasks: {person.get('current_task_count', 0)}
- Contact: {person.get('email', '')}
"""

            resources_text = ""
            for key, res in resources.items():
                resources_text += f"- {res['type']} at {res['location']}: {res['current_stock']} {res['unit']} available\n"

            ai_prompt = f"""
Create optimal task assignments for disaster response based on the following data:

PRIORITIZED REQUESTS (ordered by priority):
{requests_text}

AVAILABLE PERSONNEL:
{personnel_text}

AVAILABLE RESOURCES:
{resources_text}

Create assignments following these rules:
1. Assign highest priority requests first
2. Match personnel skills to request needs
3. Consider geographic proximity
4. Don't exceed personnel max task limits
5. Ensure resources are available before assignment
6. Create clear, actionable task instructions

Provide a JSON response:
{{
    "assignments": [
        {{
            "request_id": "request_id",
            "assignee_id": "person_id",
            "task_title": "Clear task title",
            "task_description": "Detailed instructions",
            "priority": "critical/high/medium/low",
            "estimated_duration": "time estimate",
            "required_resources": [
                {{
                    "resource_type": "type",
                    "quantity": 5,
                    "location": "location"
                }}
            ],
            "special_instructions": "any special notes",
            "contact_info": "emergency contact if needed"
        }}
    ],
    "unassigned_requests": ["list of request IDs that couldn't be assigned"],
    "assignment_summary": "overall strategy and reasoning"
}}
"""

            # Get AI response
            response = self.run(ai_prompt)
            ai_result = response.content if hasattr(response, 'content') else str(response)
            
            # Parse AI response
            import json
            try:
                ai_data = json.loads(ai_result)
                assignments = ai_data.get("assignments", [])
                
                # Validate and enhance assignments
                validated_assignments = []
                for assignment in assignments:
                    # Check if assignee exists and is available
                    assignee_id = assignment.get("assignee_id")
                    assignee = next((p for p in personnel if p.get("id") == assignee_id), None)
                    
                    if assignee:
                        # Add timestamp and status
                        assignment.update({
                            "id": f"task_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{len(validated_assignments)}",
                            "assignee_name": assignee.get("name", "Unknown"),
                            "assignee_email": assignee.get("email", ""),
                            "assignee_role": assignee.get("role", "volunteer"),
                            "status": "assigned",
                            "created_at": datetime.utcnow().isoformat(),
                            "assigned_by": "AI",
                            "due_date": None,  # Could be calculated based on priority
                            "location": assignee.get("location", "unknown")
                        })
                        validated_assignments.append(assignment)
                
                return validated_assignments
                
            except json.JSONDecodeError:
                logger.error("Failed to parse AI assignment response")
                return []
                
        except Exception as e:
            logger.error(f"AI assignment creation failed: {e}")
            return []

    def reserve_resources(self, assignments: List[Dict]) -> bool:
        """Reserve resources for assignments"""
        try:
            for assignment in assignments:
                required_resources = assignment.get("required_resources", [])
                
                for resource_req in required_resources:
                    resource_type = resource_req.get("resource_type")
                    quantity = resource_req.get("quantity", 0)
                    location = resource_req.get("location", "")
                    
                    # Find matching resource
                    resource_key = f"{resource_type}_{location}"
                    
                    # Update resource stock (simplified - in production would use proper locking)
                    response = (
                        supabase.table("resources")
                        .select("*")
                        .eq("type", resource_type)
                        .eq("location", location)
                        .gt("current_stock", quantity)
                        .execute()
                    )
                    
                    if response.data:
                        resource = response.data[0]
                        new_stock = resource["current_stock"] - quantity
                        
                        # Update stock
                        supabase.table("resources").update({
                            "current_stock": new_stock,
                            "updated_at": datetime.utcnow().isoformat()
                        }).eq("id", resource["id"]).execute()
                        
                        # Log resource allocation
                        supabase.table("resource_allocations").insert({
                            "resource_id": resource["id"],
                            "task_id": assignment.get("id"),
                            "quantity": quantity,
                            "allocated_at": datetime.utcnow().isoformat(),
                            "status": "allocated"
                        }).execute()
                        
                        logger.info(f"Reserved {quantity} {resource_type} for task {assignment.get('id')}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to reserve resources: {e}")
            return False

    def save_assignments_to_db(self, assignments: List[Dict]) -> bool:
        """Save task assignments to database"""
        try:
            for assignment in assignments:
                # Create task record
                task_data = {
                    "id": assignment.get("id"),
                    "request_id": assignment.get("request_id"),
                    "assignee_id": assignment.get("assignee_id"),
                    "title": assignment.get("task_title"),
                    "description": assignment.get("task_description"),
                    "priority": assignment.get("priority"),
                    "status": assignment.get("status"),
                    "estimated_duration": assignment.get("estimated_duration"),
                    "special_instructions": assignment.get("special_instructions"),
                    "created_at": assignment.get("created_at"),
                    "assigned_by": assignment.get("assigned_by"),
                    "due_date": assignment.get("due_date"),
                    "location": assignment.get("location")
                }
                
                # Insert task
                response = supabase.table("tasks").insert(task_data).execute()
                
                if response.data:
                    # Update request status
                    supabase.table("requests").update({
                        "status": "assigned",
                        "assigned_at": datetime.utcnow().isoformat(),
                        "assignee_id": assignment.get("assignee_id")
                    }).eq("id", assignment.get("request_id")).execute()
                    
                    logger.info(f"Created task assignment: {assignment.get('id')}")
                else:
                    logger.error(f"Failed to create task assignment: {assignment.get('id')}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save assignments to database: {e}")
            return False

    def run_assignment_cycle(self) -> Dict:
        """Run a complete assignment cycle"""
        try:
            # Get data
            requests = self.get_prioritized_requests()
            personnel = self.get_available_personnel()
            resources = self.get_available_resources()
            
            if not requests:
                return {"status": "no_requests", "assigned": 0}
            
            if not personnel:
                return {"status": "no_personnel", "pending_requests": len(requests)}
            
            # Create assignments
            assignments = self.create_assignments(requests, personnel, resources)
            
            if not assignments:
                return {"status": "no_assignments_possible", "pending_requests": len(requests)}
            
            # Reserve resources
            resources_reserved = self.reserve_resources(assignments)
            
            # Save assignments
            assignments_saved = self.save_assignments_to_db(assignments)
            
            result = {
                "status": "completed" if assignments_saved else "partial_failure",
                "assigned": len(assignments),
                "pending_requests": len(requests) - len(assignments),
                "resources_reserved": resources_reserved,
                "assignments_saved": assignments_saved,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Assignment cycle completed: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Assignment cycle failed: {e}")
            return {"status": "failed", "error": str(e)}


# Standalone functions for backward compatibility
def assign_tasks() -> Dict:
    """Run assignment for all prioritized requests"""
    agent = AssignmentAgent()
    return agent.run_assignment_cycle()


def assign_specific_request(request_id: str, assignee_id: str = None) -> Dict:
    """Assign a specific request, optionally to a specific person"""
    try:
        agent = AssignmentAgent()
        
        # Get specific request
        response = (
            supabase.table("requests")
            .select("*")
            .eq("id", request_id)
            .execute()
        )
        
        if not response.data:
            return {"status": "request_not_found", "request_id": request_id}
        
        request_data = response.data[0]
        
        # Get personnel (specific person or all available)
        if assignee_id:
            personnel_response = (
                supabase.table("users")
                .select("*")
                .eq("id", assignee_id)
                .eq("status", "available")
                .execute()
            )
            personnel = personnel_response.data if personnel_response.data else []
        else:
            personnel = agent.get_available_personnel()
        
        if not personnel:
            return {"status": "no_available_personnel", "request_id": request_id}
        
        # Get resources
        resources = agent.get_available_resources()
        
        # Create assignment
        assignments = agent.create_assignments([request_data], personnel, resources)
        
        if assignments:
            agent.reserve_resources(assignments)
            agent.save_assignments_to_db(assignments)
            return {"status": "completed", "assignment": assignments[0]}
        else:
            return {"status": "assignment_failed", "request_id": request_id}
            
    except Exception as e:
        logger.error(f"Failed to assign request {request_id}: {e}")
        return {"status": "error", "error": str(e)}
