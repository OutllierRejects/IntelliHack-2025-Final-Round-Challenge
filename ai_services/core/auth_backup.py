# ai_services/core/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.database import supabase
from models.user import UserOut
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Verify JWT token and return user data"""
    try:
        token = credentials.credentials

        # Verify with Supabase
        user_response = supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

        return {
            "id": user_response.user.id,
            "email": user_response.user.email,
            "user_metadata": user_response.user.user_metadata or {},
        }
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


async def get_current_user(token_data: dict = Depends(verify_token)) -> UserOut:
    """Get current user from database"""
    try:
        user_id = token_data["id"]

        # Get user from database
        response = supabase.table("users").select("*").eq("id", user_id).execute()

        if not response.data:
            # Create user if doesn't exist
            user_data = {
                "id": user_id,
                "email": token_data["email"],
                "full_name": token_data.get("user_metadata", {}).get("full_name", ""),
                "role": token_data.get("user_metadata", {}).get("role", "affected"),
                "status": "active",
            }

            create_response = supabase.table("users").insert(user_data).execute()
            if create_response.data:
                return UserOut(**create_response.data[0])
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user",
                )

        return UserOut(**response.data[0])
    except Exception as e:
        logger.error(f"Failed to get current user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user information",
        )


def require_role(required_roles: list):
    """Decorator to require specific roles"""

    def role_checker(current_user: UserOut = Depends(get_current_user)):
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )
        return current_user

    return role_checker
