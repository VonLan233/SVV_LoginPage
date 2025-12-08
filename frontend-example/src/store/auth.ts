/**
 * SVV-LoginPage Authentication Store
 *
 * Zustand store for managing authentication state.
 *
 * Security: JWT token is stored in HttpOnly cookie (set by backend),
 * NOT in localStorage, to prevent XSS attacks from stealing tokens.
 *
 * Features:
 * - User information storage (non-sensitive data only)
 * - Authentication state tracking
 * - Persistent user info via localStorage (token is in HttpOnly cookie)
 *
 * State:
 * - user: User object (id, username, email)
 * - isAuthenticated: Boolean flag for auth status
 *
 * Actions:
 * - login: Set user info and mark as authenticated
 * - logout: Clear all auth state
 * - updateUser: Update user information
 *
 * Storage Key: 'auth-storage' in localStorage (user info only, NOT token)
 *
 * Usage:
 *   const { user, isAuthenticated, login, logout } = useAuthStore()
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
  /** Current user information */
  user: User | null
  /** Whether user is authenticated */
  isAuthenticated: boolean
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
      user: null,
      isAuthenticated: false,

      login: (user) => set({ user, isAuthenticated: true }),

      logout: () => set({ user: null, isAuthenticated: false }),

      updateUser: (user) => set({ user }),
    }),
    {
      name: 'auth-storage', // localStorage key (stores user info only, NOT token)
    }
  )
)

export type { User, AuthState }
