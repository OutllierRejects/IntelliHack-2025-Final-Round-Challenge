# ai_services/api/endpoints/incidents.py
from fastapi import APIRouter, Depends, HTTPException
from models.incident import IncidentCreate, IncidentOut
from services.incident_service import IncidentService
from core.auth import get_current_user

router = APIRouter()


@router.post("/incidents", response_model=IncidentOut)
async def report_incident(payload: IncidentCreate, user=Depends(get_current_user)):
    try:
        # payload.reported_by = user.email  # or user.id
        incident_service = IncidentService()
        return await incident_service.create_incident(payload.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
