# ai_services/api/endpoints/incidents.py
from fastapi import APIRouter, Depends, HTTPException
from models.incident import IncidentCreate, IncidentOut
from services.incident_service import create_incident
from core.auth import get_current_user

router = APIRouter()


@router.post("/incidents", response_model=IncidentOut)
def report_incident(payload: IncidentCreate, user=Depends(get_current_user)):
    try:
        # payload.reported_by = user.email  # or user.id
        return create_incident(payload.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
