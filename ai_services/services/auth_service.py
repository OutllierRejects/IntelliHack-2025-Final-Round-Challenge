"""
Authentication service for user management and JWT tokens
"""

import jwt
import bcrypt
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from core.config import get_settings

logger = logging.getLogger(__name__)


class AuthService:
    """Service for authentication and authorization"""

    def __init__(self):
        self.settings = get_settings()

    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt

        Args:
            password: Plain text password

        Returns:
            str: Hashed password
        """
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash

        Args:
            password: Plain text password
            hashed_password: Stored hashed password

        Returns:
            bool: True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"), hashed_password.encode("utf-8")
            )
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False

    def create_access_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token

        Args:
            data: Data to encode in the token
            expires_delta: Token expiration time

        Returns:
            str: Encoded JWT token
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(hours=24)

        to_encode.update(
            {"exp": expire, "iat": datetime.now(timezone.utc), "type": "access"}
        )

        return jwt.encode(
            to_encode, self.settings.JWT_SECRET, algorithm=self.settings.JWT_ALGORITHM
        )

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """
        Create a JWT refresh token

        Args:
            data: Data to encode in the token

        Returns:
            str: Encoded JWT refresh token
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=30)

        to_encode.update(
            {"exp": expire, "iat": datetime.now(timezone.utc), "type": "refresh"}
        )

        return jwt.encode(
            to_encode, self.settings.JWT_SECRET, algorithm=self.settings.JWT_ALGORITHM
        )

    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decode and validate a JWT token

        Args:
            token: JWT token to decode

        Returns:
            Dict: Decoded token data

        Raises:
            jwt.InvalidTokenError: If token is invalid
        """
        try:
            payload = jwt.decode(
                token,
                self.settings.JWT_SECRET,
                algorithms=[self.settings.JWT_ALGORITHM],
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.InvalidTokenError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise jwt.InvalidTokenError(f"Invalid token: {e}")

    def get_current_user_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Extract user information from a valid token

        Args:
            token: JWT token

        Returns:
            Dict: User information or None if invalid
        """
        try:
            payload = self.decode_token(token)

            if payload.get("type") != "access":
                return None

            return {
                "id": payload.get("sub"),
                "email": payload.get("email"),
                "role": payload.get("role"),
                "full_name": payload.get("full_name"),
            }
        except jwt.InvalidTokenError:
            return None

    def validate_user_role(self, user_role: str, required_roles: list) -> bool:
        """
        Validate if user has required role

        Args:
            user_role: User's current role
            required_roles: List of acceptable roles

        Returns:
            bool: True if user has required role
        """
        return user_role in required_roles

    def create_user_tokens(self, user_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Create both access and refresh tokens for a user

        Args:
            user_data: User information to encode

        Returns:
            Dict: Access and refresh tokens
        """
        token_data = {
            "sub": user_data["id"],
            "email": user_data["email"],
            "role": user_data["role"],
            "full_name": user_data.get("full_name", ""),
        }

        access_token = self.create_access_token(token_data)
        refresh_token = self.create_refresh_token({"sub": user_data["id"]})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }


# Global auth service instance
_auth_service: Optional[AuthService] = None


def get_auth_service() -> AuthService:
    """Get the global auth service instance"""
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthService()
    return _auth_service


# Convenience functions
def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password using global auth service"""
    return get_auth_service().verify_password(password, hashed_password)


def create_access_token(data: Dict[str, Any]) -> str:
    """Create access token using global auth service"""
    return get_auth_service().create_access_token(data)
