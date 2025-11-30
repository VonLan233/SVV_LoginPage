# SVV-LoginPage Backend

FastAPI-based JWT authentication module with PostgreSQL and SQLAlchemy.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Configure Environment

Create a `.env` file in your project root:

```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/myapp
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Security Note**: Generate a secure SECRET_KEY:
```bash
openssl rand -hex 32
```

### 2. Initialize Database

```python
from backend.database import init_db

# Creates the users table
init_db()
```

### 3. Integrate with FastAPI

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import router

app = FastAPI(title="My App with Authentication")

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(router)

# Your other routes...
```

### 4. Run the Application

```bash
uvicorn main:app --reload
```

Visit http://localhost:8000/docs for interactive API documentation.

## API Endpoints

### POST /api/auth/token
Login and get JWT access token.

**Request Body** (form-data):
```
username: string
password: string
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=secret123"
```

### POST /api/auth/register
Register a new user.

**Request Body** (JSON):
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "secret123"
}
```

**Response**:
```json
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"secret123"}'
```

### GET /api/auth/users/me
Get current user information (requires authentication).

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response**:
```json
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Example**:
```bash
curl -X GET http://localhost:8000/api/auth/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### PUT /api/auth/users/me
Update current user information (requires authentication).

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body** (JSON, all fields optional):
```json
{
  "username": "john_new",
  "email": "john_new@example.com",
  "password": "newsecret456"
}
```

**Response**: Updated user object

## Usage Patterns

### Protecting Routes

```python
from fastapi import Depends
from backend.auth import get_current_active_user
from backend.models import User

@app.get("/protected")
async def protected_route(current_user: User = Depends(get_current_active_user)):
    return {"message": f"Hello {current_user.username}!"}
```

### Creating a User Programmatically

```python
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import User
from backend.auth import get_password_hash

db = SessionLocal()
user = User(
    username="admin",
    email="admin@example.com",
    hashed_password=get_password_hash("admin123"),
    is_superuser=True
)
db.add(user)
db.commit()
db.close()
```

### Custom Token Expiration

```python
from datetime import timedelta
from backend.auth import create_access_token

# Create a token that expires in 7 days
token = create_access_token(
    data={"sub": "username"},
    expires_delta=timedelta(days=7)
)
```

## Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | Required | PostgreSQL connection string |
| `SECRET_KEY` | Required | Secret key for JWT signing (32+ chars) |
| `ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration time in minutes |
| `APP_HOST` | `0.0.0.0` | Application host |
| `APP_PORT` | `8000` | Application port |
| `DEBUG` | `True` | Debug mode (set False in production) |

### Programmatic Configuration

```python
from backend.config import settings

# Access settings
print(settings.database_url)
print(settings.secret_key)
print(settings.access_token_expire_minutes)
```

## Database Models

### User Model

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

## Authentication Flow

1. **Registration**:
   - User submits username, email, password
   - Password is hashed with bcrypt
   - User record is created in database

2. **Login**:
   - User submits username and password
   - Password is verified against hashed password
   - JWT token is generated and returned
   - Token includes username in "sub" claim and expiration time

3. **Authenticated Requests**:
   - Client includes token in Authorization header: `Bearer <token>`
   - Request interceptor extracts and validates token
   - User object is retrieved from database and injected into route handler

4. **Logout**:
   - Client-side: Remove token from storage
   - Server-side: No action needed (stateless JWT)

## Security Best Practices

1. **Use HTTPS in Production**: Always use TLS/SSL to protect tokens in transit
2. **Strong SECRET_KEY**: Use a cryptographically secure random string (32+ bytes)
3. **Short Token Expiration**: Balance security and UX (default 30 minutes)
4. **Password Requirements**: Implement minimum length and complexity on frontend
5. **Rate Limiting**: Add rate limiting middleware to prevent brute force attacks
6. **CORS Configuration**: Only allow trusted origins

## Testing

Run tests with pytest:

```bash
pytest tests/test_auth.py -v
```

Example test:

```python
def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
```

## Troubleshooting

### Database Connection Error
```
sqlalchemy.exc.OperationalError: could not connect to server
```
**Solution**: Check DATABASE_URL is correct and PostgreSQL is running.

### JWT Decode Error
```
jose.exceptions.JWTError: Invalid token
```
**Solution**: Ensure SECRET_KEY is the same on all instances and token hasn't expired.

### Username Already Registered
```
{"detail": "Username already registered"}
```
**Solution**: This is expected behavior. Username must be unique.

## Module Structure

```
backend/
├── __init__.py       # Exports: router, models, schemas, auth functions
├── auth.py           # JWT creation, password hashing, user dependencies
├── api.py            # FastAPI router with authentication endpoints
├── models.py         # SQLAlchemy User model
├── schemas.py        # Pydantic schemas for validation
├── config.py         # Settings with environment variable support
├── database.py       # Database connection and session management
└── requirements.txt  # Python dependencies
```

## Dependencies

- **FastAPI**: Modern web framework with automatic API documentation
- **SQLAlchemy**: SQL toolkit and ORM
- **psycopg2-binary**: PostgreSQL adapter
- **python-jose**: JWT implementation
- **passlib**: Password hashing library
- **pydantic**: Data validation using Python type hints
- **python-multipart**: Form data parsing for OAuth2

## Version

1.0.0
