# ai_services/agno_agents/prioritization_agent.py
import os
import json
import logging
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from typing import Dict, List
from datetime import datetime
from core.database import supabase

logger = logging.getLogger(__name__)


class PrioritizationAgent(Agent):
    """AGNO Agent for prioritizing disaster response requests"""

    def __init__(self):
        """Initialize PrioritizationAgent with OpenAI model"""
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY environment variable is required for PrioritizationAgent"
            )

        try:
            model = OpenAIChat(
                id="gpt-4o-mini",
                temperature=0.1,
                max_tokens=1000,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI model: {e}")
            raise ValueError(f"OpenAI model initialization failed: {e}")

        super().__init__(
            name="DisasterPrioritizationAgent",
            model=model,
            description="AI agent for prioritizing disaster response requests based on urgency and resources",
            instructions="""
You are a disaster response prioritization agent. Your job is to:
1. Analyze help requests and assign priority levels (critical, high, medium, low)
2. Consider urgency factors, resource availability, and vulnerable populations
3. Factor in location proximity to available resources and responders
4. Ensure medical emergencies and life-threatening situations get highest priority

Priority Guidelines:
- CRITICAL: Life-threatening, medical emergencies, trapped individuals, fire/explosion
- HIGH: Urgent medical needs, vulnerable populations (elderly, children, disabled), severe resource shortages
- MEDIUM: Important needs but not life-threatening, moderate resource requirements
- LOW: Non-urgent requests, basic needs with adequate resources available

Always respond with valid JSON format only:
{
    "priority": "critical/high/medium/low",
    "urgency_score": 0.85,
    "resource_impact": "high/medium/low",
    "reasoning": "Brief explanation of priority decision",
    "recommended_resources": ["resource1", "resource2"],
    "estimated_response_time": "immediate/1-2 hours/4-6 hours/next day"
}
""",
            add_history_to_messages=True,
            num_history_responses=3,
            markdown=False,
        )
        self.version = "1.0.0"

        super().__init__(
            name="DisasterPrioritizationAgent",
            model=model,
            description="AI agent for prioritizing disaster response requests based on urgency, resources, and impact",
            instructions="""
You are a disaster response prioritization agent. Your job is to:
1. Analyze processed requests and assign priority scores
2. Consider resource availability and proximity
3. Factor in vulnerable populations and special needs
4. Balance urgency with available response capacity
5. Recommend priority levels: critical, high, medium, low

Use these priority criteria:
- CRITICAL: Life-threatening emergencies, imminent danger, medical emergencies
- HIGH: Serious injuries, vulnerable populations, rescue situations
- MEDIUM: Basic needs (food, water, shelter) for general population
- LOW: Non-urgent support needs, information requests

Always prioritize life-safety first, then vulnerable populations, then general welfare needs.
""",
            add_history_to_messages=True,
            num_history_responses=5,
            markdown=False,
        )
        self.version = "1.0.0"

    def get_unprocessed_requests(self) -> List[Dict]:
        """Fetch requests that need prioritization"""
        try:
            response = (
                supabase.table("requests")
                .select("*")
                .in_("status", ["processing", "new"])
                .order("created_at", desc=False)
                .execute()
            )
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Failed to fetch unprocessed requests: {e}")
            return []

    def get_resource_availability(self) -> Dict:
        """Get current resource levels"""
        try:
            response = supabase.table("resources").select("*").execute()
            resources = {}
            if response.data:
                for resource in response.data:
                    resources[resource["type"]] = {
                        "available": resource.get("quantity", 0),
                        "threshold": resource.get("threshold", 10),
                        "location": resource.get("location", "unknown"),
                    }
            return resources
        except Exception as e:
            logger.error(f"Failed to fetch resource availability: {e}")
            return {}

    def calculate_priority_factors(self, request: Dict, resources: Dict) -> Dict:
        """Calculate priority factors for a request"""
        factors = {
            "urgency_keywords": 0.0,
            "vulnerability_factor": 0.0,
            "resource_scarcity": 0.0,
            "time_factor": 0.0,
        }

        description = (
            f"{request.get('title', '')} {request.get('description', '')}".lower()
        )

        # Urgency keywords
        critical_words = [
            "emergency",
            "urgent",
            "critical",
            "dying",
            "fire",
            "explosion",
            "trapped",
            "bleeding",
        ]
        high_words = ["serious", "injured", "unconscious", "severe", "help", "pain"]

        if any(word in description for word in critical_words):
            factors["urgency_keywords"] = 1.0
        elif any(word in description for word in high_words):
            factors["urgency_keywords"] = 0.7
        else:
            factors["urgency_keywords"] = 0.3

        # Vulnerability factor
        vulnerable_words = [
            "elderly",
            "child",
            "baby",
            "pregnant",
            "disabled",
            "sick",
            "alone",
        ]
        if any(word in description for word in vulnerable_words):
            factors["vulnerability_factor"] = 0.8
        else:
            factors["vulnerability_factor"] = 0.2

        # Resource scarcity
        needs = request.get("needs", [])
        scarcity_score = 0.0
        for need in needs:
            if need in resources:
                available = resources[need]["available"]
                threshold = resources[need]["threshold"]
                if available <= threshold:
                    scarcity_score += 0.3
                elif available <= threshold * 2:
                    scarcity_score += 0.1
        factors["resource_scarcity"] = min(scarcity_score, 1.0)

        # Time factor (older requests get slightly higher priority)
        created_at = datetime.fromisoformat(
            request.get("created_at", datetime.utcnow().isoformat()).replace(
                "Z", "+00:00"
            )
        )
        hours_old = (
            datetime.utcnow().replace(tzinfo=created_at.tzinfo) - created_at
        ).total_seconds() / 3600
        factors["time_factor"] = min(hours_old * 0.05, 0.3)

        return factors

    def prioritize_request(self, request: Dict, resources: Dict) -> Dict:
        """Prioritize a single request using AI"""
        try:
            # Calculate baseline factors
            factors = self.calculate_priority_factors(request, resources)

            # Prepare context for AI
            context = {
                "request_id": request.get("id"),
                "title": request.get("title", ""),
                "description": request.get("description", ""),
                "needs": request.get("needs", []),
                "location": request.get("location", ""),
                "current_priority": request.get("priority", "medium"),
                "factors": factors,
                "available_resources": {
                    k: v["available"] for k, v in resources.items()
                },
                "resource_thresholds": {
                    k: v["threshold"] for k, v in resources.items()
                },
            }

            ai_prompt = f"""
Analyze this disaster help request and determine its priority level:

Request Details:
- Title: {context['title']}
- Description: {context['description']}
- Needs: {context['needs']}
- Location: {context['location']}

Priority Factors:
- Urgency Score: {factors['urgency_keywords']}
- Vulnerability Factor: {factors['vulnerability_factor']}
- Resource Scarcity: {factors['resource_scarcity']}
- Time Factor: {factors['time_factor']}

Available Resources: {context['available_resources']}
Resource Thresholds: {context['resource_thresholds']}

Respond with valid JSON only:
{{
    "priority": "critical/high/medium/low",
    "urgency_score": 0.85,
    "resource_impact": "high/medium/low", 
    "reasoning": "Brief explanation",
    "recommended_resources": ["resource1", "resource2"],
    "estimated_response_time": "immediate/1-2 hours/4-6 hours/next day"
}}
"""

            # Get AI response
            response = self.run(ai_prompt)
            ai_result = (
                response.content if hasattr(response, "content") else str(response)
            )

            # Parse AI result
            try:
                # Clean response
                ai_result = ai_result.strip()
                if ai_result.startswith("```json"):
                    ai_result = ai_result[7:-3].strip()
                elif ai_result.startswith("```"):
                    ai_result = ai_result[3:-3].strip()

                ai_data = json.loads(ai_result)

                # Validate and extract
                priority = ai_data.get("priority", "medium")
                urgency_score = ai_data.get("urgency_score", 0.5)
                resource_impact = ai_data.get("resource_impact", "medium")
                reasoning = ai_data.get("reasoning", "AI analysis completed")
                recommended_resources = ai_data.get("recommended_resources", [])
                estimated_response_time = ai_data.get(
                    "estimated_response_time", "4-6 hours"
                )

            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"AI response parsing failed: {e}, using fallback logic")
                # Fallback logic
                total_score = sum(factors.values()) / len(factors)
                if total_score >= 0.8:
                    priority = "critical"
                elif total_score >= 0.6:
                    priority = "high"
                elif total_score >= 0.3:
                    priority = "medium"
                else:
                    priority = "low"

                urgency_score = total_score
                resource_impact = (
                    "high" if factors["resource_scarcity"] > 0.5 else "medium"
                )
                reasoning = "Automated prioritization based on keyword analysis"
                recommended_resources = request.get("needs", [])
                estimated_response_time = "4-6 hours"

            result = {
                "request_id": request.get("id"),
                "priority": priority,
                "urgency_score": urgency_score,
                "resource_impact": resource_impact,
                "reasoning": reasoning,
                "recommended_resources": recommended_resources,
                "estimated_response_time": estimated_response_time,
                "factors": factors,
                "processed_at": datetime.utcnow().isoformat(),
                "ai_processed": True,
            }

            logger.info(f"Prioritized request {request.get('id')}: {priority} priority")
            return result

        except Exception as e:
            logger.error(f"Request prioritization failed: {e}")
            return {
                "request_id": request.get("id"),
                "priority": "medium",
                "urgency_score": 0.5,
                "resource_impact": "medium",
                "reasoning": f"Error in prioritization: {str(e)}",
                "recommended_resources": [],
                "estimated_response_time": "4-6 hours",
                "processed_at": datetime.utcnow().isoformat(),
                "ai_processed": False,
                "error": str(e),
            }

    def update_request_priority(self, prioritization_result: Dict) -> bool:
        """Update request priority in database"""
        try:
            request_id = prioritization_result["request_id"]
            update_data = {
                "priority": prioritization_result["priority"],
                "urgency_score": prioritization_result["urgency_score"],
                "estimated_response_time": prioritization_result[
                    "estimated_response_time"
                ],
                "status": "prioritized",
                "updated_at": datetime.utcnow().isoformat(),
            }

            response = (
                supabase.table("requests")
                .update(update_data)
                .eq("id", request_id)
                .execute()
            )

            if response.data:
                logger.info(f"Updated priority for request {request_id}")
                return True
            else:
                logger.error(f"Failed to update request {request_id}: No data returned")
                return False

        except Exception as e:
            logger.error(
                f"Database update failed for request {prioritization_result.get('request_id')}: {e}"
            )
            return False

    def run_prioritization_cycle(self) -> Dict:
        """Run complete prioritization cycle"""
        try:
            # Get unprocessed requests
            requests = self.get_unprocessed_requests()
            if not requests:
                logger.info("No requests to prioritize")
                return {
                    "processed": 0,
                    "errors": 0,
                    "message": "No requests to prioritize",
                }

            # Get resource availability
            resources = self.get_resource_availability()

            processed = 0
            errors = 0
            results = []

            for request in requests:
                try:
                    # Prioritize request
                    result = self.prioritize_request(request, resources)
                    results.append(result)

                    # Update database
                    if self.update_request_priority(result):
                        processed += 1
                    else:
                        errors += 1

                except Exception as e:
                    logger.error(
                        f"Failed to prioritize request {request.get('id')}: {e}"
                    )
                    errors += 1

            summary = {
                "processed": processed,
                "errors": errors,
                "total_requests": len(requests),
                "results": results,
                "timestamp": datetime.utcnow().isoformat(),
            }

            logger.info(
                f"Prioritization cycle complete: {processed} processed, {errors} errors"
            )
            return summary

        except Exception as e:
            logger.error(f"Prioritization cycle failed: {e}")
            return {
                "processed": 0,
                "errors": 1,
                "total_requests": 0,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }


# Standalone functions for backward compatibility
def prioritize_requests() -> Dict:
    """Run prioritization for all unprocessed requests"""
    agent = PrioritizationAgent()
    return agent.run_prioritization_cycle()


def prioritize_specific_request(request_id: str) -> Dict:
    """Prioritize a specific request"""
    try:
        agent = PrioritizationAgent()

        # Fetch specific request
        response = supabase.table("requests").select("*").eq("id", request_id).execute()

        if not response.data:
            return {"error": f"Request {request_id} not found"}

        request = response.data[0]
        resources = agent.get_resource_availability()

        # Prioritize and update
        result = agent.prioritize_request(request, resources)
        success = agent.update_request_priority(result)

        return {
            "success": success,
            "result": result,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Failed to prioritize specific request {request_id}: {e}")
        return {"error": str(e)}
