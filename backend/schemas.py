"""
SVV-LoginPage Pydantic Schemas
Data validation and serialization schemas for API requests/responses
"""

import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


# Validation patterns
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]+$')
# Password allowed characters: letters, digits, and special characters !@#$%^&*
PASSWORD_ALLOWED_PATTERN = re.compile(r'^[a-zA-Z0-9!@#$%^&*]+$')
PASSWORD_UPPERCASE = re.compile(r'[A-Z]')
PASSWORD_LOWERCASE = re.compile(r'[a-z]')
PASSWORD_DIGIT = re.compile(r'[0-9]')
PASSWORD_SPECIAL = re.compile(r'[!@#$%^&*]')


def validate_username(username: str) -> str:
    """Validate username contains only letters, numbers, and underscores"""
    if not USERNAME_PATTERN.match(username):
        raise ValueError('Username can only contain letters (a-z, A-Z), numbers (0-9), and underscores (_)')
    if len(username) < 3:
        raise ValueError('Username must be at least 3 characters')
    if len(username) > 50:
        raise ValueError('Username must be at most 50 characters')
    return username


def validate_password(password: str) -> str:
    """Validate password contains uppercase, lowercase, digit, and special character"""
    # Collect all validation errors
    errors = []
    
    # Check length constraints
    password_length = len(password)
    if password_length < 8:
        errors.append('be at least 8 characters long')
    if password_length > 128:
        errors.append('be at most 128 characters')
    
    # Only allow printable ASCII characters
    if any(ord(c) < 32 or ord(c) > 126 for c in password):
        raise ValueError('Password contains invalid characters. Only printable ASCII characters are allowed.')
    
    if not PASSWORD_UPPERCASE.search(password):
        errors.append('contain at least one uppercase letter')
    if not PASSWORD_LOWERCASE.search(password):
        errors.append('contain at least one lowercase letter')
    if not PASSWORD_DIGIT.search(password):
        errors.append('contain at least one digit')
    if not PASSWORD_SPECIAL.search(password):
        errors.append('contain at least one special character (!@#$%^&*)')
    
    if errors:
        raise ValueError('Password MUST: ' + '; '.join(errors))
    return password


# User Schemas
class UserBase(BaseModel):
    """Base user schema with common fields"""
    username: str
    email: EmailStr

    @field_validator('username')
    @classmethod
    def username_valid(cls, v: str) -> str:
        return validate_username(v)


class UserCreate(UserBase):
    """Schema for user registration

    Attributes:
        username: Unique username (inherited)
        email: Unique email address (inherited)
        password: Plain text password (will be hashed)
    """
    password: str

    @field_validator('password')
    @classmethod
    def password_valid(cls, v: str) -> str:
        return validate_password(v)


class UserUpdate(BaseModel):
    """Schema for updating user information

    All fields are optional. Only provided fields will be updated.
    Note: Password change is not supported in this version (no frontend UI).

    Attributes:
        username: New username (must be unique if provided)
        email: New email address (must be unique if provided)
    """
    username: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator('username')
    @classmethod
    def username_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validate_username(v)
        return v


class UserResponse(UserBase):
    """Schema for user API responses

    Attributes:
        id: User ID
        username: Username (inherited)
        email: Email address (inherited)
        is_active: Whether the user account is active
        is_superuser: Whether the user has superuser privileges
        created_at: Timestamp of account creation
    """
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy models


# Authentication Schemas
class Token(BaseModel):
    """JWT token response schema

    Attributes:
        access_token: JWT access token string
        token_type: Token type (always "bearer")
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """JWT token payload data

    Attributes:
        username: Username extracted from JWT token
    """
    username: Optional[str] = None
