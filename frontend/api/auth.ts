/**
 * SVV-LoginPage Authentication API
 *
 * API functions for authentication operations (login, register, user management).
 *
 * All functions use the apiClient which automatically includes JWT token
 * in Authorization header for authenticated requests.
 *
 * Endpoints:
 * - POST /api/auth/token - Login and get JWT token
 * - POST /api/auth/register - Register new user
 * - GET /api/auth/users/me - Get current user info
 * - PUT /api/auth/users/me - Update current user info
 */

import apiClient from './client'

// Request/Response Types
interface LoginRequest {
  username: string
  password: string
}

interface RegisterRequest {
  username: string
  email: string
  password: string
}

interface TokenResponse {
  access_token: string
  token_type: string
}

interface UserResponse {
  id: number
  username: string
  email: string
  is_active: boolean
  is_superuser: boolean
  created_at: string
}

/**
 * Authentication API functions
 */
export const authApi = {
  /**
   * Login with username and password
   * Returns JWT access token
   *
   * @param data - Login credentials
   * @returns Token response with access_token and token_type
   */
  login: async (data: LoginRequest): Promise<TokenResponse> => {
    // OAuth2 requires application/x-www-form-urlencoded format
    const params = new URLSearchParams()
    params.append('username', data.username)
    params.append('password', data.password)

    const response = await apiClient.post<TokenResponse>('/api/auth/token', params.toString(), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  /**
   * Register a new user
   *
   * @param data - User registration data (username, email, password)
   * @returns Created user information
   */
  register: async (data: RegisterRequest): Promise<UserResponse> => {
    const response = await apiClient.post<UserResponse>('/api/auth/register', data)
    return response.data
  },

  /**
   * Get current authenticated user information
   * Requires valid JWT token in Authorization header
   *
   * @returns Current user information
   */
  getCurrentUser: async (): Promise<UserResponse> => {
    const response = await apiClient.get<UserResponse>('/api/auth/users/me')
    return response.data
  },

  /**
   * Update current user information
   * Requires valid JWT token in Authorization header
   *
   * @param data - Partial user data to update (username, email, password)
   * @returns Updated user information
   */
  updateCurrentUser: async (data: Partial<RegisterRequest>): Promise<UserResponse> => {
    const response = await apiClient.put<UserResponse>('/api/auth/users/me', data)
    return response.data
  },
}

// Export types for use in other modules
export type { LoginRequest, RegisterRequest, TokenResponse, UserResponse }
