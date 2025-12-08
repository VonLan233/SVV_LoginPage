/**
 * SVV-LoginPage API Client
 *
 * Axios HTTP client with cookie-based authentication.
 *
 * Security: JWT token is stored in HttpOnly cookie (set by backend),
 * NOT in localStorage, to prevent XSS attacks from stealing tokens.
 *
 * Features:
 * - Cookie-based authentication (withCredentials: true)
 * - Configurable base URL via environment variable
 * - FormData Content-Type handling
 * - 401 response interceptor for session invalidation
 *
 * Environment Variables:
 * - VITE_API_URL: Backend API base URL (defaults to http://localhost:8000)
 *
 * Usage:
 *   import { apiClient } from './api/client'
 *   const response = await apiClient.get('/api/users/me')
 */

import axios from 'axios'
import { useAuthStore } from '../store/auth'

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
  // Enable sending cookies with cross-origin requests
  // Required for HttpOnly cookie authentication
  withCredentials: true,
})

// Request interceptor: Handle FormData Content-Type
apiClient.interceptors.request.use(
  (config) => {
    // If request data is FormData, remove Content-Type to let browser set it automatically
    // (including multipart boundary)
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }

    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor: Handle 401 errors
// Automatically logs out user and redirects to login on 401 Unauthorized
// This ensures sessions are invalidated when user is deleted or token becomes invalid
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Don't redirect on login/register failures - those 401s are expected
    const isAuthEndpoint = error.config?.url?.includes('/api/auth/token')

    if (error.response?.status === 401 && !isAuthEndpoint) {
      // Clear auth state and redirect to login
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export { apiClient }
export default apiClient
