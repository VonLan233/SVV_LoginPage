# SVV-LoginPage

A reusable, production-ready authentication module with both frontend (React + TypeScript) and backend (FastAPI + SQLAlchemy) components.

## Features

### Backend
- ✅ **JWT Authentication**: Secure token-based authentication with configurable expiration
- ✅ **Bcrypt Password Hashing**: Industry-standard password security
- ✅ **OAuth2 Compatible**: Standard OAuth2 password flow
- ✅ **User Management**: Complete CRUD operations for user accounts
- ✅ **PostgreSQL Database**: SQLAlchemy ORM with async support
- ✅ **FastAPI Framework**: Modern, fast web framework with automatic API documentation

### Frontend
- ✅ **React Components**: Ready-to-use Login and Register pages
- ✅ **Form Validation**: React Hook Form + Zod schema validation
- ✅ **State Management**: Zustand with localStorage persistence
- ✅ **Type Safety**: Full TypeScript support
- ✅ **API Client**: Axios with JWT token auto-injection
- ✅ **UI Components**: shadcn/ui integration for beautiful design

## Quick Start

### Docker Deployment
```bash
docker-compose up -d --build
```

### Backend Integration

1. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
# Create .env file
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. **Initialize Database**
```python
from backend.database import init_db
init_db()  # Creates users table
```

4. **Add to FastAPI App**
```python
from fastapi import FastAPI
from backend import router

app = FastAPI()
app.include_router(router)  # Adds /api/auth/* endpoints
```

See [backend/README.md](backend/README.md) for detailed documentation.

### Frontend Integration

1. **Install Dependencies**
```bash
npm install axios zustand @tanstack/react-query react-hook-form zod @hookform/resolvers
```

2. **Configure API URL**
```bash
# Add to .env
VITE_API_URL=http://localhost:8000
```

3. **Add to React Router**
```tsx
import { Login, Register } from 'svv-loginpage/frontend'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  )
}
```

4. **Use Auth Store**
```tsx
import { useAuthStore } from 'svv-loginpage/frontend'

function MyComponent() {
  const { isAuthenticated, user, logout } = useAuthStore()

  return isAuthenticated ? (
    <div>Welcome {user?.username}! <button onClick={logout}>Logout</button></div>
  ) : (
    <Link to="/login">Login</Link>
  )
}
```

See [frontend/README.md](frontend/README.md) for detailed documentation.

## Project Structure

```
SVV-LoginPage/
├── backend/                 # Backend module
│   ├── __init__.py         # Module exports
│   ├── auth.py             # JWT authentication core
│   ├── api.py              # API routes (login, register, user CRUD)
│   ├── models.py           # SQLAlchemy User model
│   ├── schemas.py          # Pydantic schemas
│   ├── config.py           # Settings and configuration
│   ├── database.py         # Database connection
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Backend documentation
│
├── frontend/                # Frontend module
│   ├── components/         # React components
│   │   ├── Login.tsx      # Login page component
│   │   └── Register.tsx   # Register page component
│   ├── api/               # API client
│   │   ├── client.ts      # Axios instance with interceptors
│   │   └── auth.ts        # Authentication API functions
│   ├── store/             # State management
│   │   └── auth.ts        # Zustand auth store
│   ├── types/             # TypeScript types
│   │   └── auth.ts        # Shared type definitions
│   ├── index.ts           # Module exports
│   ├── package.json       # Dependencies
│   └── README.md         # Frontend documentation
│
├── migrations/            # Database migrations
│   └── create_users_table.sql
│
├── tests/                 # Test files
│   └── test_auth.py
│
└── README.md             # This file
```

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/token` | Login and get JWT token | No |
| POST | `/api/auth/register` | Register new user | No |
| GET | `/api/auth/users/me` | Get current user info | Yes |
| PUT | `/api/auth/users/me` | Update current user | Yes |

## Security Features

- **Bcrypt Password Hashing**: Passwords are never stored in plain text
- **JWT Tokens**: Stateless authentication with configurable expiration
- **CORS Support**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic and Zod schema validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **Unique Constraints**: Username and email uniqueness enforced at DB level

## Configuration

### Backend Environment Variables

```bash
# Required
DATABASE_URL=postgresql://user:pass@host:port/dbname
SECRET_KEY=your-secret-key-minimum-32-characters

# Optional
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
```

### Frontend Environment Variables

```bash
# Required
VITE_API_URL=http://localhost:8000
```

## Database Schema

### Users Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| username | VARCHAR(100) | UNIQUE, NOT NULL |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| hashed_password | VARCHAR(255) | NOT NULL |
| is_active | BOOLEAN | DEFAULT TRUE |
| is_superuser | BOOLEAN | DEFAULT FALSE |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | ON UPDATE NOW() |

## Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend (manual testing recommended)
# Start both backend and frontend, test user flows
```

## License

MIT License

## Support

For issues, questions, or contributions, please refer to the project repository.

## Dependencies

### Backend
- FastAPI 0.104+
- SQLAlchemy 2.0+
- python-jose (JWT)
- passlib (bcrypt)
- PostgreSQL

### Frontend
- React 18+
- TypeScript 5+
- Axios
- Zustand
- React Hook Form + Zod
- TanStack Query
- shadcn/ui components

## Version

1.0.0 - Initial release
1.0.1 - Feature updates
