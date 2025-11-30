# SVV-LoginPage Frontend

React + TypeScript authentication components with Zustand state management and React Hook Form validation.

## Installation

```bash
npm install axios zustand @tanstack/react-query react-hook-form zod @hookform/resolvers react-router-dom
```

## Quick Start

### 1. Configure API URL

Create or update `.env` in your React project root:

```bash
VITE_API_URL=http://localhost:8000
```

### 2. Setup React Query Provider

Wrap your app with QueryClientProvider:

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      {/* Your app */}
    </QueryClientProvider>
  )
}
```

### 3. Add Routes

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Login, Register } from 'svv-loginpage/frontend'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        {/* Your other routes */}
      </Routes>
    </BrowserRouter>
  )
}
```

### 4. Use Authentication State

```tsx
import { useAuthStore } from 'svv-loginpage/frontend'

function MyComponent() {
  const { isAuthenticated, user, logout } = useAuthStore()

  if (!isAuthenticated) {
    return <Navigate to="/login" />
  }

  return (
    <div>
      <h1>Welcome, {user?.username}!</h1>
      <button onClick={logout}>Logout</button>
    </div>
  )
}
```

## Components

### Login Component

Full-featured login page with form validation and error handling.

**Props**:
```typescript
interface LoginPageProps {
  redirectPath?: string                    // Default: '/dashboard'
  onLoginSuccess?: (user: User) => void    // Optional callback
}
```

**Usage**:
```tsx
import { Login } from 'svv-loginpage/frontend'

<Login
  redirectPath="/home"
  onLoginSuccess={(user) => console.log('Logged in:', user)}
/>
```

**Features**:
- Username and password validation
- Toast notifications
- Loading states
- Automatic token storage
- User info fetching
- Redirect after login

### Register Component

Registration page with email validation and password confirmation.

**Props**:
```typescript
interface RegisterPageProps {
  redirectPath?: string       // Default: '/login'
  onRegisterSuccess?: () => void    // Optional callback
}
```

**Usage**:
```tsx
import { Register } from 'svv-loginpage/frontend'

<Register
  redirectPath="/login"
  onRegisterSuccess={() => console.log('Registration complete')}
/>
```

**Features**:
- Username validation (min 3 chars)
- Email format validation
- Password strength (min 6 chars)
- Password confirmation matching
- Toast notifications
- Redirect to login after registration

## State Management

### Auth Store (Zustand)

Zustand store with localStorage persistence.

**State**:
```typescript
interface AuthState {
  token: string | null
  user: User | null
  isAuthenticated: boolean
  setToken: (token: string) => void
  login: (user: User) => void
  logout: () => void
  updateUser: (user: User) => void
}
```

**Usage Examples**:

```tsx
import { useAuthStore } from 'svv-loginpage/frontend'

// Get auth state
const { isAuthenticated, user } = useAuthStore()

// Login (called by Login component)
const { login, setToken } = useAuthStore()
setToken(tokenResponse.access_token)
login(userInfo)

// Logout
const { logout } = useAuthStore()
logout()  // Clears token, user, and isAuthenticated

// Update user info
const { updateUser } = useAuthStore()
updateUser({ ...user, email: 'newemail@example.com' })

// Check authentication
if (isAuthenticated) {
  // User is logged in
}
```

**Persistence**:
- Store key: `auth-storage` in localStorage
- Persists across browser sessions
- Automatically rehydrates on app load

## API Client

### Axios Instance

Pre-configured Axios instance with JWT token injection.

```typescript
import { apiClient } from 'svv-loginpage/frontend'

// GET request (token automatically added)
const response = await apiClient.get('/api/users/me')

// POST request
const response = await apiClient.post('/api/data', { foo: 'bar' })

// PUT request
const response = await apiClient.put('/api/users/me', { email: 'new@email.com' })
```

**Features**:
- Automatic JWT token in Authorization header
- Base URL from environment variable
- FormData Content-Type handling
- 30 second timeout

### Auth API Functions

Pre-built API functions for authentication operations.

```typescript
import { authApi } from 'svv-loginpage/frontend'

// Login
const tokenResponse = await authApi.login({
  username: 'john',
  password: 'secret123'
})
// Returns: { access_token: string, token_type: 'bearer' }

// Register
const user = await authApi.register({
  username: 'john',
  email: 'john@example.com',
  password: 'secret123'
})
// Returns: UserResponse

// Get current user
const user = await authApi.getCurrentUser()
// Returns: UserResponse

// Update current user
const updatedUser = await authApi.updateCurrentUser({
  email: 'newemail@example.com'
})
// Returns: UserResponse
```

## Protected Routes

Protect routes that require authentication:

```tsx
import { Navigate } from 'react-router-dom'
import { useAuthStore } from 'svv-loginpage/frontend'

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuthStore()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return children
}

// Usage in routes
<Route path="/dashboard" element={
  <ProtectedRoute>
    <Dashboard />
  </ProtectedRoute>
} />
```

## Advanced Usage

### Custom Login Handler

```tsx
import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { authApi, useAuthStore } from 'svv-loginpage/frontend'

function CustomLoginForm() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const { setToken, login } = useAuthStore()

  const loginMutation = useMutation({
    mutationFn: authApi.login,
    onSuccess: async (data) => {
      setToken(data.access_token)
      const userInfo = await authApi.getCurrentUser()
      login(userInfo)
      // Custom logic here
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    loginMutation.mutate({ username, password })
  }

  return <form onSubmit={handleSubmit}>...</form>
}
```

### Checking User Permissions

```tsx
import { useAuthStore } from 'svv-loginpage/frontend'

function AdminPanel() {
  const { user } = useAuthStore()

  if (!user?.is_superuser) {
    return <div>Access denied. Admin only.</div>
  }

  return <div>Admin panel content...</div>
}
```

### Redirect with Query Parameters

```tsx
// Login with redirect parameter
<Link to="/login?redirect=/dashboard">Login</Link>

// Login component automatically handles redirect
// User will be sent to /dashboard after successful login
```

## Styling

Components use [shadcn/ui](https://ui.shadcn.com/) design system. You'll need:

### Required Components
- Button
- Input
- Label

### Setup shadcn/ui

```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button input label
```

### Custom Styling

To customize styles, override Tailwind classes:

```tsx
import { Login } from 'svv-loginpage/frontend'

// Custom wrapper
<div className="custom-auth-page">
  <Login />
</div>
```

Or modify the component files directly in your project.

## TypeScript Types

All types are exported for use in your application:

```typescript
import type {
  User,
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  UserResponse,
  AuthState
} from 'svv-loginpage/frontend'

// Use in your components
const user: User = {
  id: 1,
  username: 'john',
  email: 'john@example.com'
}

// Type-safe API calls
const loginData: LoginRequest = {
  username: 'john',
  password: 'secret'
}
```

## Error Handling

### API Errors

```tsx
import { authApi } from 'svv-loginpage/frontend'
import { useToast } from '@/hooks/use-toast'

const { toast } = useToast()

try {
  await authApi.login({ username, password })
} catch (error: any) {
  toast({
    variant: 'destructive',
    title: 'Login failed',
    description: error.response?.data?.detail || 'Network error'
  })
}
```

### Form Validation Errors

Form validation errors are automatically displayed below each input field.

```tsx
// Validation schema in Login.tsx
const loginSchema = z.object({
  username: z.string().min(1, 'Username is required'),
  password: z.string().min(1, 'Password is required'),
})
```

## Testing

### Component Testing

```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import { Login } from 'svv-loginpage/frontend'

test('renders login form', () => {
  const queryClient = new QueryClient()

  render(
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    </QueryClientProvider>
  )

  expect(screen.getByLabelText(/username/i)).toBeInTheDocument()
  expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
})
```

### Store Testing

```tsx
import { useAuthStore } from 'svv-loginpage/frontend'

test('login updates auth state', () => {
  const { login, isAuthenticated, user } = useAuthStore.getState()

  login({ id: 1, username: 'test', email: 'test@example.com' })

  const state = useAuthStore.getState()
  expect(state.isAuthenticated).toBe(true)
  expect(state.user?.username).toBe('test')
})
```

## Troubleshooting

### "Network Error" on Login
- Check `VITE_API_URL` is correct
- Ensure backend is running
- Check browser console for CORS errors

### Token Not Persisting
- Check browser localStorage for `auth-storage`
- Ensure no localStorage clearing on navigation
- Check for third-party cookie blockers

### Components Not Rendering
- Verify all peer dependencies are installed
- Check React version (needs 18+)
- Ensure shadcn/ui components are installed

### Type Errors
- Update TypeScript to 5.0+
- Check `tsconfig.json` includes proper module resolution

## Module Structure

```
frontend/
├── components/
│   ├── Login.tsx        # Login page component
│   └── Register.tsx     # Register page component
├── api/
│   ├── client.ts        # Axios instance with interceptors
│   └── auth.ts          # Authentication API functions
├── store/
│   └── auth.ts          # Zustand authentication store
├── types/
│   └── auth.ts          # TypeScript type definitions
├── index.ts             # Main exports
├── package.json         # Dependencies
└── README.md           # This file
```

## Dependencies

- **react**: ^18.2.0
- **react-router-dom**: ^6.20.0
- **axios**: ^1.6.2
- **zustand**: ^4.4.7
- **@tanstack/react-query**: ^5.14.0
- **react-hook-form**: ^7.48.2
- **zod**: ^3.22.4
- **@hookform/resolvers**: ^3.3.2

## Version

1.0.0
