# ai_services/services/incident_service.py
from agno_agents.triage_agent import triage_incident
from core.database import supabase
from uuid import uuid4
from datetime import datetime

def create_incident(data: dict) -> dict:
    priority = triage_incident(data["description"])
    incident_id = str(uuid4())
    
    new_incident = {
        "id": incident_id,
        "title": data["title"],
        "description": data["description"],
        "location": data.get("location"),
        "reporter_id": data.get("reporter_id"),
        "priority": priority,
        "created_at": datetime.utcnow().isoformat()
    }
    
    response = supabase.table("incidents").insert(new_incident).execute()
    return response.data[0] if response.data else new_incident


if __name__ == "__main__":
    sample_data = {
        "title": "Unauthorized Access Detected",
        "description": "An unknown individual was seen entering the restricted server room.",
        "location": "Server Room 3",
        "reported_by": "John Doe"
    }
    result = create_incident(sample_data)
    print(result)