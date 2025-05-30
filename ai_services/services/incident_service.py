# ai_services/services/incident_service.py
from agno_agents.triage_agent import triage_incident
from core.database import supabase
from uuid import uuid4
from datetime import datetime

def create_incident(data: dict) -> dict:
    severity = triage_incident(data["description"])
    incident_id = str(uuid4())
    
    new_incident = {
        "id": incident_id,
        "title": data["title"],
        "description": data["description"],
        "location": data.get("location"),
        "reported_by": data.get("reported_by"),
        "severity": severity,
        "created_at": datetime.utcnow().isoformat()
    }
    
    response = supabase.table("incidents").insert(new_incident).execute()
    return response.data[0] if response.data else new_incident
