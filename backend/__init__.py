"""
SVV-LoginPage Backend Module
JWT-based authentication system for FastAPI applications
"""

__version__ = "1.0.0"

from backend.api import router
from backend.auth import (
    get_current_user,
    get_current_active_user,
    get_password_hash,
    verify_password,
    create_access_token,
)
from backend.models import User
from backend.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    Token,
    TokenData,
)
from backend.database import get_db, init_db

__all__ = [
    "router",
    "get_current_user",
    "get_current_active_user",
    "get_password_hash",
    "verify_password",
    "create_access_token",
    "User",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "Token",
    "TokenData",
    "get_db",
    "init_db",
]
