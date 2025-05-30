from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel, EmailStr
from core.auth import get_current_user
from core.database import supabase  # Assuming supabase client is initialized in core/database.py
from supabase import Client

router = APIRouter()

# Request schemas
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Route: Register user
@router.post("/register")
def register_user(payload: RegisterRequest):
    try:
        result = supabase.auth.sign_up(
            {
                "email": payload.email,
                "password": payload.password
            }
        )
        return {"message": "User registered successfully", "user": result.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Route: Login user
@router.post("/login")
def login_user(payload: LoginRequest):
    try:
        result = supabase.auth.sign_in_with_password(
            {
                "email": payload.email,
                "password": payload.password
            }
        )
        if result.session is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token,
            "user": result.user
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


# Route: Get current user profile
@router.get("/profile")
def get_profile(user=Depends(get_current_user)):
    return {"user": user}
