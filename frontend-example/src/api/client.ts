/**
 * SVV-LoginPage API Client
 *
 * Axios HTTP client with JWT authentication interceptor.
 *
 * Features:
 * - Automatic JWT token injection in Authorization header
 * - Configurable base URL via environment variable
 * - FormData Content-Type handling
 * - Optional 401 response interceptor (commented out)
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
})

// Request interceptor: Add JWT token to Authorization header
apiClient.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // If request data is FormData, remove Content-Type to let browser set it automatically
    // (including multipart boundary)
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }

    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor: Handle 401 errors (optional, uncomment to enable)
// Automatically logs out user and redirects to login on 401 Unauthorized
/*
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear auth state and redirect to login
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
*/

export { apiClient }
export default apiClient
