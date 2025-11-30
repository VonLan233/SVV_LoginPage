"""
SVV-LoginPage Authentication Tests

Test suite for authentication API endpoints.

Usage:
    pytest tests/test_auth.py -v
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.models import User
from backend.auth import get_password_hash
from backend.api import router

# Create test database engine (in-memory SQLite for testing)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Test fixtures
@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(db_session):
    """Create test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)

    from backend.database import get_db
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def create_test_user(db_session, username="testuser", email="test@example.com", password="testpass"):
    """Helper function to create a test user"""
    user = User(
        username=username,
        email=email,
        hashed_password=get_password_hash(password),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# Tests
class TestRegistration:
    """Test user registration endpoint"""

    def test_register_success(self, client, db_session):
        """Test successful user registration"""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass123"
        }

        response = client.post("/api/auth/register", json=user_data)

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["username"] == "newuser"
        assert response_data["email"] == "newuser@example.com"
        assert "id" in response_data
        assert "hashed_password" not in response_data  # Should not expose password

        # Verify user was created in database
        db_user = db_session.query(User).filter(User.username == "newuser").first()
        assert db_user is not None
        assert db_user.email == "newuser@example.com"
        assert db_user.hashed_password != "newpass123"  # Should be hashed

    def test_register_duplicate_username(self, client, db_session):
        """Test registration with duplicate username"""
        # Create existing user
        create_test_user(db_session, username="existing", email="existing@example.com")

        # Try to register with same username
        user_data = {
            "username": "existing",
            "email": "newemail@example.com",
            "password": "testpass123"
        }

        response = client.post("/api/auth/register", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Username already registered" in response.json()["detail"]

    def test_register_duplicate_email(self, client, db_session):
        """Test registration with duplicate email"""
        # Create existing user
        create_test_user(db_session, username="existing", email="existing@example.com")

        # Try to register with same email
        user_data = {
            "username": "newuser",
            "email": "existing@example.com",
            "password": "testpass123"
        }

        response = client.post("/api/auth/register", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]


class TestLogin:
    """Test user login endpoint"""

    def test_login_success(self, client, db_session):
        """Test successful login"""
        # Create test user
        password = "testpass123"
        create_test_user(db_session, username="loginuser", password=password)

        # Login
        login_data = {
            "username": "loginuser",
            "password": password
        }

        response = client.post("/api/auth/token", data=login_data)

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, db_session):
        """Test login with incorrect password"""
        # Create test user
        create_test_user(db_session, username="loginuser", password="correctpass")

        # Try to login with wrong password
        login_data = {
            "username": "loginuser",
            "password": "wrongpass"
        }

        response = client.post("/api/auth/token", data=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, client, db_session):
        """Test login with non-existent username"""
        login_data = {
            "username": "nonexistent",
            "password": "anypass"
        }

        response = client.post("/api/auth/token", data=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]


class TestCurrentUser:
    """Test get current user endpoint"""

    def test_get_current_user_success(self, client, db_session):
        """Test getting current user info with valid token"""
        # Create user and login
        password = "testpass123"
        user = create_test_user(db_session, username="testuser", email="test@example.com", password=password)

        # Get token
        login_response = client.post("/api/auth/token", data={"username": "testuser", "password": password})
        token = login_response.json()["access_token"]

        # Get user info
        response = client.get(
            "/api/auth/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["username"] == "testuser"
        assert response_data["email"] == "test@example.com"
        assert response_data["id"] == user.id

    def test_get_current_user_no_token(self, client):
        """Test getting current user without token"""
        response = client.get("/api/auth/users/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token"""
        response = client.get(
            "/api/auth/users/me",
            headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestUpdateUser:
    """Test update current user endpoint"""

    def test_update_user_email(self, client, db_session):
        """Test updating user email"""
        # Create user and login
        password = "testpass123"
        user = create_test_user(db_session, username="testuser", password=password)

        # Get token
        login_response = client.post("/api/auth/token", data={"username": "testuser", "password": password})
        token = login_response.json()["access_token"]

        # Update email
        update_data = {"email": "newemail@example.com"}
        response = client.put(
            "/api/auth/users/me",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["email"] == "newemail@example.com"

        # Verify in database
        db_session.refresh(user)
        assert user.email == "newemail@example.com"

    def test_update_user_username(self, client, db_session):
        """Test updating username"""
        # Create user and login
        password = "testpass123"
        user = create_test_user(db_session, username="oldname", password=password)

        # Get token
        login_response = client.post("/api/auth/token", data={"username": "oldname", "password": password})
        token = login_response.json()["access_token"]

        # Update username
        update_data = {"username": "newname"}
        response = client.put(
            "/api/auth/users/me",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["username"] == "newname"

        # Verify in database
        db_session.refresh(user)
        assert user.username == "newname"

    def test_update_user_duplicate_email(self, client, db_session):
        """Test updating to an email that already exists"""
        # Create two users
        password = "testpass123"
        create_test_user(db_session, username="user1", email="user1@example.com", password=password)
        create_test_user(db_session, username="user2", email="user2@example.com", password=password)

        # Login as user1
        login_response = client.post("/api/auth/token", data={"username": "user1", "password": password})
        token = login_response.json()["access_token"]

        # Try to update to user2's email
        update_data = {"email": "user2@example.com"}
        response = client.put(
            "/api/auth/users/me",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
