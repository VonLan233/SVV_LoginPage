# SVV-LoginPage Quick Start Guide

Get up and running with SVV-LoginPage in 5 minutes!

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL database

## Backend Setup (2 minutes)

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Create .env file
cp ../.env.example ../.env

# Edit .env with your database credentials
# DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

### 3. Initialize Database

```bash
# Create tables
python ../migrations/init_db.py

# Optionally create admin user
python ../migrations/init_db.py --create-admin
```

### 4. Start Backend

```python
# Create main.py in your project root
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import router

app = FastAPI(title="My App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```bash
# Run the server
python main.py
```

Visit http://localhost:8000/docs to see the API documentation!

## Frontend Setup (3 minutes)

### 1. Install Dependencies

```bash
cd frontend
npm install axios zustand @tanstack/react-query react-hook-form zod @hookform/resolvers
```

### 2. Setup shadcn/ui (if not already installed)

```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button input label
```

### 3. Configure API URL

```bash
# Add to your React project's .env
echo "VITE_API_URL=http://localhost:8000" >> .env
```

### 4. Add to Your React App

```tsx
// App.tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Login, Register, useAuthStore } from 'svv-loginpage/frontend'

const queryClient = new QueryClient()

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuthStore()
  return isAuthenticated ? children : <Navigate to="/login" />
}

function Dashboard() {
  const { user, logout } = useAuthStore()
  return (
    <div>
      <h1>Welcome {user?.username}!</h1>
      <button onClick={logout}>Logout</button>
    </div>
  )
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />
          <Route path="/" element={<Navigate to="/dashboard" />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
```

### 5. Start Frontend

```bash
npm run dev
```

Visit http://localhost:5173 to see your app!

## Test It Out

1. **Register a new account**:
   - Go to http://localhost:5173/register
   - Fill in username, email, and password
   - Click "Register"

2. **Login**:
   - You'll be redirected to login page
   - Enter your credentials
   - Click "Login"

3. **Access Protected Route**:
   - After login, you'll be redirected to /dashboard
   - Your username will be displayed
   - Try refreshing the page - you'll stay logged in!

4. **Logout**:
   - Click the "Logout" button
   - You'll be logged out and redirected to login

## API Endpoints

Test the API directly:

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"secret123"}'

# Login
curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=secret123"

# Get current user (replace TOKEN with the access_token from login)
curl http://localhost:8000/api/auth/users/me \
  -H "Authorization: Bearer TOKEN"
```

## Troubleshooting

### Backend Issues

**Database connection error**:
```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT 1"

# Verify DATABASE_URL in .env is correct
```

**Module import errors**:
```bash
# Ensure you're in the correct directory
# backend/ should be importable from your working directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Frontend Issues

**"Module not found" errors**:
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**CORS errors**:
```python
# Ensure CORS middleware is configured in your FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Token not persisting**:
- Check browser localStorage for 'auth-storage' key
- Clear localStorage and try logging in again
- Disable third-party cookie blockers

## Next Steps

- Read the full [Backend Documentation](backend/README.md)
- Read the full [Frontend Documentation](frontend/README.md)
- Customize the components to match your design
- Add additional user fields to the User model
- Implement password reset functionality
- Add email verification
- Set up proper production environment variables

## Production Checklist

Before deploying to production:

- [ ] Change SECRET_KEY to a cryptographically secure random string
- [ ] Set DEBUG=False
- [ ] Use HTTPS/TLS for all connections
- [ ] Set up proper CORS origins (don't use "*")
- [ ] Use a production-grade PostgreSQL instance
- [ ] Add rate limiting to prevent brute force attacks
- [ ] Implement password strength requirements
- [ ] Add logging and monitoring
- [ ] Set up automated backups
- [ ] Configure proper session timeouts

## Support

For issues or questions, refer to:
- [Main README](README.md)
- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)

Happy coding! 🚀
