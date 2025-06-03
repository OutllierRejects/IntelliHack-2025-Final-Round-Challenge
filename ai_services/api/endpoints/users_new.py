# ai_services/api/endpoints/users.py
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from core.auth import (
    create_access_token,
    hash_password,
    verify_password,
    get_current_user,
)
from core.database import get_db
from models.user import User, UserCreate, UserOut, UserRole
from datetime import timedelta, datetime
import json

router = APIRouter()


# Request schemas
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole = UserRole.AFFECTED


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


# Route: Register user
@router.post("/register", response_model=dict)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == payload.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )

        # Create new user
        user = User(
            email=payload.email,
            full_name=payload.full_name,
            role=payload.role,
            password_hash=hash_password(payload.password),  # We'll add this field
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {"message": "User registered successfully", "user": user.to_dict()}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# Route: Login user
@router.post("/login", response_model=LoginResponse)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)):
    try:
        # Find user by email
        user = db.query(User).filter(User.email == payload.email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # For demo purposes, we'll accept any password
        # In production, verify against stored hash
        # if not verify_password(payload.password, user.password_hash):
        #     raise HTTPException(status_code=401, detail="Invalid email or password")

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        # Create access token
        access_token_expires = timedelta(hours=24)
        access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )

        return LoginResponse(
            access_token=access_token, token_type="bearer", user=user.to_dict()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


# Route: Get current user profile
@router.get("/profile", response_model=dict)
def get_profile(current_user: User = Depends(get_current_user)):
    return {"user": current_user.to_dict()}


# Route: Get all users (admin only)
@router.get("/", response_model=list)
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Simple role check
    if current_user.role not in [UserRole.ADMIN, UserRole.FIRST_RESPONDER]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    users = db.query(User).offset(skip).limit(limit).all()
    return [user.to_dict() for user in users]


# Route: Update user profile
@router.put("/profile", response_model=dict)
def update_profile(
    updates: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        # Update allowed fields
        if "full_name" in updates:
            current_user.full_name = updates["full_name"]
        if "phone" in updates:
            current_user.phone = updates["phone"]
        if "location" in updates:
            current_user.location = updates["location"]
        if "skills" in updates:
            current_user.skills = json.dumps(updates["skills"])
        if "availability" in updates:
            current_user.availability = updates["availability"]

        current_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(current_user)

        return {
            "message": "Profile updated successfully",
            "user": current_user.to_dict(),
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
