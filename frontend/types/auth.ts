/**
 * SVV-LoginPage TypeScript Type Definitions
 *
 * Shared TypeScript interfaces and types for authentication
 */

// User Types
export interface User {
  id: number
  username: string
  email: string
  is_active?: boolean
  is_superuser?: boolean
  created_at?: string
}

// API Request Types
export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
}

export interface UpdateUserRequest {
  username?: string
  email?: string
  password?: string
}

// API Response Types
export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface UserResponse extends User {
  created_at: string
}

// Auth Store Types
export interface AuthState {
  token: string | null
  user: User | null
  isAuthenticated: boolean
  setToken: (token: string) => void
  login: (user: User) => void
  logout: () => void
  updateUser: (user: User) => void
}

// Component Prop Types
export interface LoginPageProps {
  redirectPath?: string
  onLoginSuccess?: (user: User) => void
}

export interface RegisterPageProps {
  redirectPath?: string
  onRegisterSuccess?: () => void
}
