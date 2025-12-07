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

## Bugs (For Testing/Educational Purposes)

This codebase contains intentional security vulnerabilities for software verification and validation testing.

### Bug 1: Timing Side-Channel Attack Vulnerability

**File**: `backend/auth.py` - `authenticate_user()` function (lines 37-52)

**Description**: The authentication function returns immediately when a username doesn't exist, but performs bcrypt password verification (which takes ~100-300ms) when the username exists. This timing difference allows attackers to enumerate valid usernames by measuring response times.

**How to Test**:
```bash
# Test non-existent user (fast response ~5ms)
time curl -X POST "http://localhost:8000/api/auth/token" \
  -d "username=nonexistent&password=test"

# Test existing user with wrong password (slow response ~200ms)
time curl -X POST "http://localhost:8000/api/auth/token" \
  -d "username=realuser&password=wrongpass"
```

**Fix**: Always execute bcrypt verification even for non-existent users using a dummy hash.

---

### Bug 2: Login Rate Limiting by IP Instead of Username

**File**: `backend/api.py` - `failed_login_attempts` and rate limiting functions

**Description**: Failed login attempts are tracked by client IP address instead of username. This design flaw causes:
- Multiple users behind the same NAT/VPN/corporate proxy affect each other
- Attackers can bypass lockout by rotating IP addresses (proxies, VPN)
- Legitimate users may be locked out due to shared IP with malicious actors

**How to Test**:
1. From the same IP, try logging in with different usernames using wrong passwords
2. After 5 attempts, all login attempts from that IP will be blocked
3. Users from other IPs can still attack the same account without restriction

**Fix**: Track failed attempts by username (with IP as secondary factor).

---

### Bug 3: X-Forwarded-For Header Trust Vulnerability

**File**: `backend/api.py` - `get_client_ip()` function (lines 30-36)

**Description**: The server blindly trusts the `X-Forwarded-For` HTTP header to determine client IP. Attackers can bypass IP-based rate limiting by simply setting a fake header.

**How to Test**:
```bash
# Bypass rate limiting by spoofing different IPs
for i in {1..10}; do
  curl -X POST "http://localhost:8000/api/auth/token" \
    -H "X-Forwarded-For: 192.168.1.$i" \
    -d "username=victim&password=attempt$i"
done
```

**Fix**: Only trust X-Forwarded-For when behind a trusted reverse proxy, validate the header chain.

---

### Bug 4: User Can Modify Own is_active Status

**File**: `backend/api.py` - `update_user_me()` function (lines 239-241)

**Description**: The user update endpoint allows users to set their own `is_active` status. While currently inactive users cannot call this endpoint (blocked by `get_current_active_user`), this creates a privilege escalation path if combined with other vulnerabilities.

**How to Test**:
```bash
curl -X PUT "http://localhost:8000/api/auth/users/me" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}'
```

**Fix**: Remove `is_active` handling from user self-update, restrict to admin endpoints.

---

### Bug 5: Email Case-Sensitivity Inconsistency

**File**: `backend/api.py` - `register_user()` vs `update_user_me()`

**Description**: Email uniqueness check uses case-insensitive matching (`ilike`) during registration but case-sensitive matching during update. This allows:
- User A registers with "User@Example.com"
- User B cannot register with "user@example.com" (blocked by ilike)
- But User C can UPDATE their email to "USER@EXAMPLE.COM" (not blocked)

**How to Test**:
1. Register user A with email "Test@Example.com"
2. Register user B with a different email
3. User B updates their email to "test@example.com" - succeeds!
4. Now two users have effectively the same email

**Fix**: Use consistent case-insensitive comparison (`.ilike()`) in both registration and update.

---

### Bug 6: Password Change Does Not Invalidate Existing Tokens

**File**: `backend/auth.py` and `backend/api.py`

**Description**: JWT tokens remain valid after password change until natural expiration. If a user's credentials are compromised:
1. Attacker gets valid token
2. User changes password
3. Attacker's token still works for remaining lifetime (default 30 min)

**How to Test**:
1. Login and save the token
2. Update password via PUT /api/auth/users/me
3. Use old token - still works!

**Fix**: Include password hash version or `iat` claim in token, validate on each request; or implement token blacklist.

---

### Bug 7: Username Change Invalidates JWT Token

**File**: `backend/auth.py` - `get_current_user()` and JWT creation

**Description**: JWT tokens store username in the `sub` claim. When a user changes their username:
1. Old token contains old username
2. Token validation looks up user by `sub` (old username)
3. User not found → 401 Unauthorized

This forces immediate logout on username change, which may be unexpected.

**How to Test**:
1. Login and save the token
2. Update username via PUT /api/auth/users/me
3. Use old token → 401 Unauthorized

**Fix**: Store user ID instead of username in JWT `sub` claim.

---

### Bug 8: Password Length Validation Uses Bytes Instead of Characters

**File**: `backend/schemas.py` - `validate_password()` function

**Description**: Password length validation uses `len(password.encode('utf-8'))` which counts bytes, not characters. While currently the password only allows ASCII characters, this creates inconsistency:
- "12345678" = 8 bytes, 8 chars ✓
- If UTF-8 chars were allowed: "密码12345" = 13 bytes, 7 chars → would pass length check incorrectly

**How to Test**: Currently minimal impact due to ASCII-only restriction, but creates technical debt.

**Fix**: Use `len(password)` for character count.

---

### Bug 9: Registration Race Condition (TOCTOU)

**File**: `backend/api.py` - `register_user()` function

**Description**: Time-of-check to time-of-use vulnerability. Between checking username uniqueness and inserting the user, another concurrent request could insert the same username.

**How to Test**:
```bash
# Send two registration requests simultaneously
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"racetest","email":"race1@test.com","password":"Test123!"}' &
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"racetest","email":"race2@test.com","password":"Test123!"}'
```

**Fix**: Use database-level unique constraints (already present) and handle IntegrityError, or use SELECT FOR UPDATE.

---

### Bug 10: Frontend isLoading State Not Reset After Success

**File**: `frontend-example/src/components/Register.tsx` - `registerMutation.onSuccess`

**Description**: In the registration form's `onSuccess` callback, `setIsLoading(false)` is never called. The submit button remains in "Registering..." disabled state until navigation completes. If navigation is slow or fails, the UI appears stuck.

**How to Test**:
1. Fill out the registration form with valid data
2. Submit the form
3. Observe the button stays as "Registering..." even after success toast appears
4. The loading state only resets when the page navigates away or on error

**Fix**: Add `setIsLoading(false)` before the toast notification in onSuccess callback.

---

### Bug 11: Login Does Not Check User is_active Status 🔴 CRITICAL

**File**: `backend/api.py` - `login_for_access_token()` function

**Description**: The login endpoint does not verify if the user account is active before issuing a JWT token. This means:
- Admin disables a user account (`is_active=False`)
- User can still login and receive a valid JWT token
- Token only gets rejected when used (in `get_current_active_user`)

This is a serious security flaw - disabled accounts should be rejected at login time.

**How to Test**:
```bash
# 1. Create a user and get their ID
# 2. Disable the user in database: UPDATE users SET is_active=false WHERE username='testuser'
# 3. Try to login - it will succeed!
curl -X POST "http://localhost:8000/api/auth/token" \
  -d "username=testuser&password=Test123!"
# Returns valid token instead of error
```

**Fix**: Add is_active check after authentication:
```python
user = authenticate_user(db, form_data.username, form_data.password)
if not user:
    raise HTTPException(...)
if not user.is_active:
    raise HTTPException(status_code=403, detail="Account is inactive")
```

---

### Bug 12: Frontend Login Missing Rate Limit Warning

**File**: `frontend/components/Login.tsx`

**Description**: The backend implements login attempt limiting (5 failures = 1 min lockout), but the frontend Login component doesn't display any warning about remaining attempts or handle 429 status code properly.

**How to Test**:
1. Attempt login with wrong password multiple times
2. No warning is shown about remaining attempts
3. When locked out (429), error message may not be user-friendly

**Fix**: Add attempt counter display and proper 429 handling in the Login component.

---

### Bug 13: Frontend 429 Status Code Handling Incomplete

**File**: `frontend-example/src/components/Login.tsx` - `onError` handler

**Description**: The login error handler shows warning on every error, not distinguishing between 401 (wrong password) and 429 (locked out). The `showWarning` state is set for all errors.

**How to Test**:
```typescript
// Current code always shows warning
onError: (error: any) => {
  setShowWarning(true)  // Shows even for first wrong password
  // Should only show when approaching limit or for 429
}
```

**Fix**: Check error status code and show appropriate messages:
- 401: Show remaining attempts warning only when close to limit
- 429: Show lockout message with retry time

---

### Bug 14: Update User Missing Error Handling and Transaction Rollback

**File**: `backend/api.py` - `update_user_me()` function

**Description**: The user update endpoint lacks try-except error handling. If `db.commit()` fails (connection issues, constraint violations), there's no rollback mechanism.

**How to Test**:
1. Trigger a database constraint violation during update
2. Observe unhandled exception instead of proper error response

**Fix**: Wrap database operations in try-except with rollback:
```python
try:
    db.commit()
    db.refresh(current_user)
except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=400, detail="Update failed")
```

---

### Bug 15: Frontend FormData vs URLSearchParams OAuth2 Incompatibility

**File**: `frontend/api/auth.ts` - `login()` function

**Description**: The login function uses `FormData` which sends `multipart/form-data`, but OAuth2 specification requires `application/x-www-form-urlencoded`. The manually set Content-Type header is ignored by browsers when using FormData.

**How to Test**:
```typescript
// Current code (incorrect)
const formData = new FormData()  // Uses multipart/form-data
formData.append('username', data.username)
// Content-Type header is ignored

// Network tab shows: Content-Type: multipart/form-data
// OAuth2 requires: Content-Type: application/x-www-form-urlencoded
```

**Fix**: Use URLSearchParams instead:
```typescript
const params = new URLSearchParams()
params.append('username', data.username)
params.append('password', data.password)
```

---

### Bug 16: Login Attempt Counter Memory Leak

**File**: `backend/api.py` - `failed_login_attempts` dictionary

**Description**: The `failed_login_attempts` dictionary grows indefinitely without cleanup. Failed attempts are only cleared on successful login or when a locked user tries again after expiry. This causes:
- Memory leak over time
- No cleanup for users who never successfully login
- Issues in multi-instance deployments (each instance has separate counter)

**How to Test**:
```python
# After many failed login attempts from different IPs
print(len(failed_login_attempts))  # Grows forever
```

**Fix**: 
- Implement periodic cleanup of expired entries
- Use Redis or database for persistent, shared storage
- Add maximum size limit with LRU eviction

---

### Bug 17: datetime.utcnow() Deprecated in Python 3.12+

**File**: `backend/auth.py` and `backend/api.py`

**Description**: `datetime.utcnow()` is deprecated in Python 3.12+ and will be removed in future versions. Should use timezone-aware `datetime.now(timezone.utc)` instead.

**Locations**:
- `backend/auth.py` lines 78, 80
- `backend/api.py` lines 44, 60

**How to Test**:
```bash
# Run with Python 3.12+
python -W default::DeprecationWarning -c "from datetime import datetime; datetime.utcnow()"
# Shows: DeprecationWarning: datetime.utcnow() is deprecated
```

**Fix**:
```python
from datetime import datetime, timezone

# Replace
expire = datetime.utcnow() + expires_delta
# With
expire = datetime.now(timezone.utc) + expires_delta
```

---

### Bug 18: JWT Token Stored in LocalStorage (XSS Risk)

**File**: `frontend-example/src/store/auth.ts`

**Description**: The authentication state (including JWT Token) is persisted to `localStorage` using `zustand`'s persist middleware. This makes the token vulnerable to theft via Cross-Site Scripting (XSS) attacks.

**How to Test**:
1. Login to the application
2. Open browser developer tools -> Application -> Local Storage
3. Observe the `auth-storage` key containing the plain text access token
4. Inject a script: `alert(localStorage.getItem('auth-storage'))` to simulate theft

**Fix**: Store tokens in HttpOnly cookies, or keep them in memory (with a refresh token mechanism in HttpOnly cookies).

---

### Bug 19: Hardcoded Secret Key in Configuration

**File**: `backend/config.py`

**Description**: The `SECRET_KEY` has a default hardcoded value. If the `SECRET_KEY` environment variable is not set in production, the application will use this known default, allowing attackers to forge valid tokens.

**How to Test**:
1. Run the backend without setting `SECRET_KEY` env var
2. Generate a valid token using the default key from `config.py`
3. Use this token to access protected endpoints

**Fix**: Raise an error if `SECRET_KEY` is not set in production; remove the default value.

---

### Bug 20: Password Change Without Old Password Verification

**File**: `backend/api.py` - `update_user_me()` function

**Description**: The user update endpoint allows setting a new password without providing the current password. If an attacker hijacks a user's session (e.g., via XSS), they can change the password and take over the account completely.

**How to Test**:
1. Login as a user
2. Send a PUT request to `/api/auth/users/me` with only `{"password": "newpassword"}`
3. The password is changed without verification

**Fix**: Require `current_password` field when updating `password`.

---

### Bug 21: Debug Mode Enabled by Default

**File**: `backend/config.py`

**Description**: The application defaults to `DEBUG=True` if the environment variable is not set. In production, this can leak sensitive information like stack traces, environment variables, and configuration details on errors.

**How to Test**:
1. Run backend without `DEBUG` env var
2. Trigger an unhandled exception
3. Observe detailed traceback in response

**Fix**: Default to `DEBUG=False`.

---

### Bug 22: Password Character Restrictions Too Strict

**File**: `backend/schemas.py`

**Description**: The password regex `^[a-zA-Z0-9!@#$%^&*]+$` allows only a specific set of special characters. This reduces password entropy and usability by banning characters like spaces, brackets, or other safe symbols.

**How to Test**:
1. Try to register with password "Correct Horse Battery Staple" (spaces)
2. Try to register with "Password123+" (plus sign)
3. Both are rejected despite being secure

**Fix**: Allow all printable ASCII characters or Unicode characters.

---

### Bug 23: Rate Limit Reset Logic Flaw

**File**: `backend/api.py` - `clear_failed_login()`

**Description**: A single successful login completely clears the failed attempt counter. An attacker with one valid account can use it to reset the IP-based lock, allowing them to continue brute-forcing other accounts from the same IP without waiting for the lockout to expire.

**How to Test**:
1. Fail login 4 times for User A
2. Login successfully once with User B (from same IP)
3. Fail login 4 times for User A again
4. The IP is never locked out

**Fix**: Do not clear global/IP-based counters on successful login for a specific user; track failures per-user/IP independently.

---

### Bug 24: Email Length 255 Characters Causes Service Crash

**File**: `backend/models.py` vs `backend/schemas.py`

**Description**: Registering a user with an email address of exactly 255 characters causes an Internal Server Error (500). This is likely due to a boundary condition error where the database column limit (VARCHAR(255)) is strictly enforced, but the application validation or driver handling fails to handle the maximum length correctly, or there is an off-by-one error in the backend logic.

**How to Test**:
```bash
# Create an email of exactly 255 characters
# 243 'a's + @example.com (12 chars) = 255 chars
LONG_EMAIL=$(python3 -c "print('a'*243 + '@example.com')")

curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"crash_test\",\"email\":\"$LONG_EMAIL\",\"password\":\"Test123!\"}"
```

**Fix**: Ensure consistent length validation between Pydantic schemas and Database models. If the DB column is VARCHAR(255), the schema should strictly validate `max_length=255` (or less to be safe).

---

## Bug Summary

### 🔓 Hidden Defects (7 Intentionally Preserved for Testing)

| # | Bug | Severity | Type |
|---|-----|----------|------|
| 1 | Timing Side-Channel Attack | 🔴 High | Security |
| 2 | IP-based Rate Limiting | 🔴 High | Security |
| 3 | X-Forwarded-For Trust | 🔴 High | Security |
| 6 | Password Change Token Valid | 🔴 High | Security |
| 18 | JWT Stored in LocalStorage | 🔴 High | Security |
| 19 | Hardcoded Secret Key | 🔴 High | Security |
| 24 | Email 255 Chars Crash | 🔴 High | Stability |

### ✅ Fixed Bugs (16 Resolved)

| # | Bug | Status |
|---|-----|--------|
| 4 | User Can Set is_active | ✅ Fixed |
| 5 | Email Case Inconsistency | ✅ Fixed |
| 7 | Username Change Breaks Token | ✅ Fixed |
| 8 | Password Length Bytes vs Chars | ✅ Fixed |
| 9 | Registration TOCTOU | ✅ Fixed |
| 10 | Frontend isLoading Not Reset | ✅ Fixed |
| 11 | Login No is_active Check | ✅ Fixed |
| 12 | Frontend Missing Rate Limit Warning | ✅ Fixed |
| 13 | Frontend 429 Handling | ✅ Fixed |
| 14 | Update Missing Error Handling | ✅ Fixed |
| 15 | FormData OAuth2 Incompatibility | ✅ Fixed |
| 16 | Memory Leak in Login Counter | ✅ Fixed |
| 17 | datetime.utcnow() Deprecated | ✅ Fixed |
| 20 | Update Password No Verification | 🗑️ Removed (no frontend UI) |
| 21 | Debug Mode Default True | ✅ Fixed |
| 22 | Strict Password Regex | ✅ Fixed |
| 23 | Rate Limit Reset Flaw | ✅ Fixed |

**Total: 7 Hidden Defects Remaining** (All High Severity)

---

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
1.0.1 - Bug added