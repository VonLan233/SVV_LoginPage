"""
SVV-LoginPage API Routes
Authentication endpoints for login, register, and user management
"""

from datetime import datetime, timedelta, timezone
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.auth import authenticate_user, create_access_token, get_current_active_user, get_password_hash
from backend.config import settings
from backend.database import get_db
from backend.models import User
from backend.schemas import Token, UserCreate, UserResponse, UserUpdate

router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"],
    responses={401: {"description": "Unauthorized"}},
)

# Rate limiting for login attempts by IP address
failed_login_attempts: Dict[str, Dict] = {}
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 1
MAX_TRACKED_IPS = 10000  # Limit memory usage


def get_client_ip(request: Request) -> str:
    """Get client IP address from request"""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def cleanup_expired_attempts():
    """Periodically clean up expired login attempt records"""
    now = datetime.now(timezone.utc)
    expired_keys = []
    for identifier, attempt_info in failed_login_attempts.items():
        locked_until = attempt_info.get("locked_until")
        if locked_until and now > locked_until:
            expired_keys.append(identifier)
    for key in expired_keys:
        del failed_login_attempts[key]
    
    # If still too many entries, remove oldest ones
    if len(failed_login_attempts) > MAX_TRACKED_IPS:
        # Remove entries that don't have active lockouts
        for identifier in list(failed_login_attempts.keys()):
            if not failed_login_attempts[identifier].get("locked_until"):
                del failed_login_attempts[identifier]
            if len(failed_login_attempts) <= MAX_TRACKED_IPS:
                break


def check_login_lockout(identifier: str) -> bool:
    """Check if identifier is locked out due to failed login attempts"""
    cleanup_expired_attempts()
    if identifier in failed_login_attempts:
        attempt_info = failed_login_attempts[identifier]
        if attempt_info.get("locked_until"):
            if datetime.now(timezone.utc) < attempt_info["locked_until"]:
                return True
            else:
                # Lock expired, reset
                del failed_login_attempts[identifier]
    return False


def record_failed_login(identifier: str):
    """Record failed login attempt for rate limiting"""
    if identifier not in failed_login_attempts:
        failed_login_attempts[identifier] = {"count": 0, "locked_until": None}
    
    failed_login_attempts[identifier]["count"] += 1
    
    if failed_login_attempts[identifier]["count"] >= MAX_LOGIN_ATTEMPTS:
        failed_login_attempts[identifier]["locked_until"] = datetime.now(timezone.utc) + timedelta(minutes=LOCKOUT_DURATION_MINUTES)


def clear_failed_login(identifier: str):
    """Clear failed login attempts after successful login"""
    if identifier in failed_login_attempts:
        del failed_login_attempts[identifier]


@router.post("/token", response_model=Token)
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login and get JWT access token

    OAuth2 compatible token login, returns JWT access token.
    Use the token in subsequent requests with Authorization: Bearer {token}

    Args:
        request: FastAPI request object
        form_data: OAuth2 form with username and password
        db: Database session

    Returns:
        Token object with access_token and token_type

    Raises:
        HTTPException: If credentials are invalid or IP is locked
    """
    client_ip = get_client_ip(request)
    
    # Check rate limiting by IP
    if check_login_lockout(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts, please try again later",
        )
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        record_failed_login(client_ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user account is active before issuing token
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Please contact administrator.",
        )
    
    # Clear failed attempts on successful login
    clear_failed_login(client_ip)
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
async def register_user(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user

    Create a new user account with username, email, and password.
    Username and email must be unique.

    Args:
        user_create: User creation data (username, email, password)
        db: Database session

    Returns:
        UserResponse object with created user details

    Raises:
        HTTPException: If username or email already exists
    """
    # Check if username already exists
    db_user = db.query(User).filter(User.username == user_create.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email already exists (case-insensitive for better UX)
    db_user = db.query(User).filter(
        User.email.ilike(user_create.email)
    ).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user with hashed password
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password
    )
    
    # Handle race condition with try-except for IntegrityError
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
        if 'username' in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        elif 'email' in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed due to constraint violation"
            )
    
    return db_user


@router.get("/users/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user information

    Returns the profile information of the currently authenticated user.

    Args:
        current_user: Current authenticated user from JWT token

    Returns:
        UserResponse object with user details
    """
    return current_user


@router.put("/users/me", response_model=UserResponse)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current user information

    Update username and/or email for the authenticated user.
    All fields are optional. Username and email must remain unique.
    Note: Password change is not supported (no frontend UI).

    Args:
        user_update: User update data (optional username, email)
        current_user: Current authenticated user from JWT token
        db: Database session

    Returns:
        UserResponse object with updated user details

    Raises:
        HTTPException: If new username or email already exists
    """
    # Update username if provided and different
    if user_update.username and user_update.username != current_user.username:
        # Check if new username already exists
        db_user = db.query(User).filter(User.username == user_update.username).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        current_user.username = user_update.username

    # Update email if provided and different (case-insensitive comparison)
    if user_update.email and user_update.email.lower() != current_user.email.lower():
        db_user = db.query(User).filter(User.email.ilike(user_update.email)).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = user_update.email

    # Commit with error handling
    try:
        db.commit()
        db.refresh(current_user)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Update failed due to constraint violation"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )
    
    return current_user
