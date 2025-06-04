"""Incident service handling incident records."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List
from uuid import uuid4

from agno_agents.triage_agent import triage_incident
from core.database import supabase
from typing import Optional


class IncidentService:
    """Service for incident management."""

    async def create_incident(self, data: Dict[str, Any]) -> Dict[str, Any]:
        priority = triage_incident(data.get("description", ""))
        incident = {
            "id": str(uuid4()),
            "title": data.get("title"),
            "description": data.get("description"),
            "location": data.get("location"),
            "incident_type": data.get("incident_type"),
            "severity": data.get("severity"),
            "status": "ACTIVE",
            "priority": priority,
            "created_at": datetime.utcnow().isoformat(),
        }
        response = supabase.table("incidents").insert(incident).execute()
        return response.data[0] if response.data else incident

    async def get_incidents_by_status(self, status: str) -> List[Dict[str, Any]]:
        response = (
            supabase.table("incidents")
            .select("*")
            .eq("status", status)
            .execute()
        )
        return response.data

    async def update_status(self, incident_id: int | str, status: str) -> Dict[str, Any]:
        response = (
            supabase.table("incidents")
            .update({"status": status, "resolved_at": datetime.utcnow().isoformat()})
            .eq("id", incident_id)
            .execute()
        )
        return response.data[0] if response.data else {}

    def calculate_priority(self, incident: Dict[str, Any]) -> int:
        severity = incident.get("severity", "LOW").upper()
        location_risk = incident.get("location_risk", "LOW").upper()
        resource = incident.get("resource_availability", "HIGH").upper()

        score = 0
        if severity == "HIGH":
            score += 50
        elif severity == "MEDIUM":
            score += 30
        else:
            score += 10

        if location_risk == "HIGH":
            score += 30
        elif location_risk == "MEDIUM":
            score += 20
        else:
            score += 10

        if resource == "LOW":
            score += 20
        elif resource == "MEDIUM":
            score += 10

        return score


# Global incident service instance
_incident_service: Optional[IncidentService] = None


def get_incident_service() -> IncidentService:
    """Retrieve the shared incident service instance."""
    global _incident_service
    if _incident_service is None:
        _incident_service = IncidentService()
    return _incident_service


async def create_incident(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience wrapper to create an incident."""
    return await get_incident_service().create_incident(data)
