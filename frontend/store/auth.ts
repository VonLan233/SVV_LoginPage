/**
 * SVV-LoginPage Authentication Store
 *
 * Zustand store for managing authentication state with localStorage persistence.
 *
 * Features:
 * - JWT token storage
 * - User information storage
 * - Authentication state tracking
 * - Persistent storage via localStorage
 *
 * State:
 * - token: JWT access token string
 * - user: User object (id, username, email)
 * - isAuthenticated: Boolean flag for auth status
 *
 * Actions:
 * - setToken: Store JWT token
 * - login: Set user info and mark as authenticated
 * - logout: Clear all auth state
 * - updateUser: Update user information
 *
 * Storage Key: 'auth-storage' in localStorage
 *
 * Usage:
 *   const { token, user, isAuthenticated, login, logout } = useAuthStore()
 */

import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: number
  username: string
  email: string
  is_active?: boolean
  is_superuser?: boolean
}

interface AuthState {
  /** JWT access token */
  token: string | null
  /** Current user information */
  user: User | null
  /** Whether user is authenticated */
  isAuthenticated: boolean
  /** Store JWT token */
  setToken: (token: string) => void
  /** Log in user with user info */
  login: (user: User) => void
  /** Log out user and clear all auth state */
  logout: () => void
  /** Update user information */
  updateUser: (user: User) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      isAuthenticated: false,

      setToken: (token) => set({ token }),

      login: (user) => set({ user, isAuthenticated: true }),

      logout: () => set({ token: null, user: null, isAuthenticated: false }),

      updateUser: (user) => set({ user }),
    }),
    {
      name: 'auth-storage', // localStorage key
    }
  )
)

export type { User, AuthState }
