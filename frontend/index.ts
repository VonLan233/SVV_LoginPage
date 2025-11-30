/**
 * SVV-LoginPage Frontend Module
 *
 * Main entry point for importing authentication components and utilities.
 *
 * Usage:
 *   import { Login, Register, useAuthStore, authApi } from 'svv-loginpage/frontend'
 */

// Components
export { default as Login } from './components/Login'
export { default as Register } from './components/Register'

// API Client
export { apiClient } from './api/client'
export { authApi } from './api/auth'

// Store
export { useAuthStore } from './store/auth'

// Types
export type {
  User,
  LoginRequest,
  RegisterRequest,
  UpdateUserRequest,
  TokenResponse,
  UserResponse,
  AuthState,
  LoginPageProps,
  RegisterPageProps,
} from './types/auth'
