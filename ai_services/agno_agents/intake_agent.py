"""
Disaster Response Intake Agent
Uses AGNO framework with OpenAI models for intelligent help request processing
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
import re
import json
from typing import Dict, List, Optional
from datetime import datetime
from core.database import supabase
import logging
import os

logger = logging.getLogger(__name__)


class IntakeAgent(Agent):
    """AGNO Agent for processing and extracting information from help requests"""

    def __init__(self):
        """Initialize IntakeAgent with OpenAI model only"""
        # Validate OpenAI API key
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is required for IntakeAgent")
        
        try:
            # Initialize OpenAI model with error handling
            model = OpenAIChat(
                id="gpt-4o-mini",
                temperature=0.1,  # Low temperature for consistent structured output
                max_tokens=1000,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI model: {e}")
            raise ValueError(f"OpenAI model initialization failed: {e}")
        
        super().__init__(
            name="DisasterIntakeAgent",
            model=model,
            description="AI agent for processing disaster help requests and extracting key information",
            instructions="""
You are a disaster response intake agent. Your job is to:
1. Analyze incoming help requests and extract key information
2. Determine the type of needs (food, water, medical, shelter, rescue, transport)
3. Assess urgency level (critical, high, medium, low)
4. Extract location information
5. Identify any special requirements or vulnerable populations

Be concise, accurate, and prioritize safety. If medical emergencies are detected, always mark as critical priority.

IMPORTANT: Always respond with valid JSON format only. Do not include any additional text or explanations.

Response format:
{
    "needs": ["list of needs like food, water, medical, shelter, rescue, transport"],
    "urgency": "critical/high/medium/low",
    "location": "extracted location or null",
    "priority": "critical/high/medium/low", 
    "special_requirements": "any vulnerable populations or special needs",
    "confidence_score": 0.85
}
""",
            add_history_to_messages=True,
            num_history_responses=3,
            markdown=False
        )
        self.version = "1.0.0"

    def extract_needs(self, description: str) -> List[str]:
        """Extract needs from request description using keyword matching"""
        needs = []
        need_keywords = {
            "food": ["food", "hungry", "meal", "eat", "nutrition", "bread", "rice"],
            "water": ["water", "thirsty", "drink", "dehydrated", "bottle"],
            "medical": [
                "medical",
                "medicine",
                "doctor",
                "hospital",
                "injury",
                "sick",
                "pain",
                "emergency",
            ],
            "shelter": [
                "shelter",
                "homeless",
                "roof",
                "house",
                "cold",
                "rain",
                "place to stay",
            ],
            "rescue": [
                "rescue",
                "trapped",
                "stuck",
                "help",
                "emergency",
                "danger",
                "fire",
            ],
            "transport": ["transport", "vehicle", "car", "bus", "evacuation", "move"],
        }

        description_lower = description.lower()
        for need_type, keywords in need_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                needs.append(need_type)
        return list(set(needs)) if needs else ["other"]

    def extract_location(self, text: str) -> Optional[str]:
        """Extract location from text using simple patterns"""
        # Look for common location patterns
        location_patterns = [
            r"at ([^,.]+)",
            r"in ([^,.]+)",
            r"near ([^,.]+)",
            r"location:?\s*([^,.]+)",
            r"address:?\s*([^,.]+)",
        ]

        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def assess_urgency(self, description: str) -> str:
        """Assess urgency level based on keywords"""
        description_lower = description.lower()

        critical_keywords = [
            "emergency",
            "urgent",
            "critical",
            "dying",
            "fire",
            "explosion",
            "trapped",
        ]
        high_keywords = ["serious", "injured", "bleeding", "unconscious", "severe"]
        medium_keywords = ["hurt", "pain", "sick", "need help"]

        if any(keyword in description_lower for keyword in critical_keywords):
            return "critical"
        elif any(keyword in description_lower for keyword in high_keywords):
            return "high"
        elif any(keyword in description_lower for keyword in medium_keywords):
            return "medium"
        else:
            return "low"

    def determine_request_type(self, needs: List[str]) -> str:
        """Determine primary request type based on needs"""
        priority_order = [
            "medical",
            "rescue",
            "food",
            "water",
            "shelter",
            "transport",
            "other",
        ]

        for req_type in priority_order:
            if req_type in needs:
                return req_type
        return "other"

    def process_request(self, request_data: Dict) -> Dict:
        """Main processing function for incoming requests using AI"""
        try:
            description = request_data.get("description", "")
            title = request_data.get("title", "")
            full_text = f"{title} {description}".strip()
            ai_prompt = f"""
Analyze this disaster help request and extract structured information:

Title: {title}
Description: {description}

Respond with valid JSON only:
{{
    "needs": ["food", "water", "medical", "shelter", "rescue", "transport"],
    "urgency": "critical/high/medium/low",
    "location": "extracted location or null",
    "priority": "critical/high/medium/low",
    "special_requirements": "vulnerable populations or special needs",
    "confidence_score": 0.85
}}
"""
            try:
                response = self.run(ai_prompt)
                ai_result = response.content if hasattr(response, 'content') else str(response)
                ai_result = ai_result.strip()
                if ai_result.startswith('```json'):
                    ai_result = ai_result[7:-3].strip()
                elif ai_result.startswith('```'):
                    ai_result = ai_result[3:-3].strip()
                ai_data = json.loads(ai_result)
                needs = ai_data.get("needs", [])
                if not isinstance(needs, list):
                    needs = [needs] if needs else []
                urgency = ai_data.get("urgency", "medium")
                extracted_location = ai_data.get("location")
                if extracted_location == "null":
                    extracted_location = None
                priority = ai_data.get("priority", "medium")
                special_requirements = ai_data.get("special_requirements", "")
                confidence_score = ai_data.get("confidence_score", 0.5)
            except (json.JSONDecodeError, AttributeError, KeyError):
                needs = self.extract_needs(full_text)
                extracted_location = self.extract_location(full_text)
                urgency = self.assess_urgency(full_text)
                priority = urgency
                special_requirements = ""
                confidence_score = 0.3
            request_type = self.determine_request_type(needs)
            if request_type in ["medical", "rescue"] and priority in ["medium", "low"]:
                priority = "high"
                urgency = "high"
            processed_data = {
                "needs": needs,
                "request_type": request_type,
                "priority": priority,
                "urgency_level": urgency,
                "extracted_location": extracted_location or request_data.get("location"),
                "special_requirements": special_requirements,
                "processed_at": datetime.utcnow().isoformat(),
                "status": "processing",
                "ai_processed": True,
                "confidence_score": confidence_score
            }
            logger.info(f"IntakeAgent processed request: {processed_data}")
            return processed_data
        except Exception as e:
            logger.error(f"IntakeAgent processing failed: {e}")
            needs = self.extract_needs(f"{request_data.get('title', '')} {request_data.get('description', '')}")
            return {
                "needs": needs,
                "request_type": self.determine_request_type(needs),
                "priority": "medium",
                "urgency_level": "medium",
                "extracted_location": request_data.get("location"),
                "special_requirements": "",
                "processed_at": datetime.utcnow().isoformat(),
                "status": "processing",
                "error": str(e),
                "ai_processed": False,
                "confidence_score": 0.1
            }

    def update_request_in_db(self, request_id: str, processed_data: Dict) -> bool:
        """Update request in database with processed information"""
        try:
            update_data = {
                "needs": processed_data["needs"],
                "request_type": processed_data["request_type"],
                "priority": processed_data["priority"],
                "urgency_level": processed_data["urgency_level"],
                "status": processed_data["status"],
                "updated_at": datetime.utcnow().isoformat(),
            }
            if processed_data.get("extracted_location"):
                update_data["location"] = processed_data["extracted_location"]
            response = (
                supabase.table("requests")
                .update(update_data)
                .eq("id", request_id)
                .execute()
            )
            if response.data:
                logger.info(f"IntakeAgent updated request {request_id} in database")
                return True
            else:
                logger.error(f"Failed to update request {request_id}: No data returned")
                return False
        except Exception as e:
            logger.error(f"IntakeAgent database update failed for request {request_id}: {e}")
            return False


# Standalone function for backward compatibility
def process_intake(request_id: str, request_data: Dict) -> Dict:
    """Process intake for a help request"""
    agent = IntakeAgent()
    processed_data = agent.process_request(request_data)

    # Update database
    success = agent.update_request_in_db(request_id, processed_data)
    processed_data["db_updated"] = success

    return processed_data
