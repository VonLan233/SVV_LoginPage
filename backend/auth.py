"""
SVV-LoginPage Authentication Module
JWT-based authentication with bcrypt password hashing
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend.config import settings
from backend.database import get_db
from backend.models import User
from backend.schemas import TokenData

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate bcrypt hash for a password"""
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user with username and password

    Args:
        db: Database session
        username: Username to authenticate
        password: Plain text password

    Returns:
        User object if authentication succeeds, False otherwise
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token

    Args:
        data: Data to encode in the token (typically {"sub": user_id})
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Get current user from JWT token

    Dependency function that extracts and validates JWT token,
    then retrieves the corresponding user from database.

    Args:
        token: JWT token from Authorization header
        db: Database session

    Returns:
        User object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user

    Dependency function that checks if the authenticated user is active.

    Args:
        current_user: User object from get_current_user dependency

    Returns:
        User object

    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_user_optional(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user, returns None if authentication fails

    Optional dependency that doesn't raise exceptions on auth failure.
    Useful for endpoints that work differently for authenticated vs anonymous users.

    Args:
        token: JWT token from Authorization header
        db: Database session

    Returns:
        User object if authenticated, None otherwise
    """
    try:
        user = await get_current_user(token, db)
        return user
    except HTTPException:
        return None


async def get_current_active_user_optional(
    current_user: User = Depends(get_current_user_optional),
) -> Optional[User]:
    """Get current active user, returns None if authentication fails or user is inactive

    Args:
        current_user: User object from get_current_user_optional dependency

    Returns:
        User object if active and authenticated, None otherwise

    Raises:
        HTTPException: If user exists but is inactive
    """
    if current_user and not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
