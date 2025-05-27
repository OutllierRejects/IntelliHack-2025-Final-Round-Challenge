from fastapi import APIRouter, Request, HTTPException
from shared.supabase_client import supabase
from shared.auth_utils import verify_jwt

router = APIRouter()

@router.get("/me")
async def get_current_user(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Token required")

    user = verify_jwt(token)
    return {"user": user}
