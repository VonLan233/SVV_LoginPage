/**
 * SVV-LoginPage Login Component
 *
 * A complete login form with React Hook Form validation, JWT authentication,
 * and state management integration.
 *
 * Features:
 * - Form validation with Zod schema
 * - JWT token storage and management
 * - User info fetching and state updates
 * - Toast notifications for feedback
 * - Redirect support after login
 *
 * Dependencies:
 * - react-hook-form: Form management
 * - zod: Schema validation
 * - @tanstack/react-query: API state management
 * - react-router-dom: Navigation
 * - shadcn/ui: UI components (Button, Input, Label)
 */

import { useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { useMutation } from '@tanstack/react-query'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'

import { useAuthStore } from '../store/auth'
import { authApi } from '../api/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useToast } from '@/hooks/use-toast'

// Form validation schema
const loginSchema = z.object({
  username: z.string().min(1, 'Username is required').max(100, 'Username is too long'),
  password: z.string().min(1, 'Password is required').max(128, 'Password is too long'),
})

type LoginFormValues = z.infer<typeof loginSchema>

interface LoginPageProps {
  /** Optional custom redirect path after successful login */
  redirectPath?: string
  /** Optional callback after successful login */
  onLoginSuccess?: (user: any) => void
}

const LoginPage = ({ redirectPath = '/dashboard', onLoginSuccess }: LoginPageProps) => {
  const [isLoading, setIsLoading] = useState(false)
  const [showWarning, setShowWarning] = useState(false)
  const [isLockedOut, setIsLockedOut] = useState(false)
  const [searchParams] = useSearchParams()
  const { setToken, login } = useAuthStore()
  const navigate = useNavigate()
  const { toast } = useToast()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  })

  const loginMutation = useMutation({
    mutationFn: authApi.login,
    onSuccess: async (data) => {
      try {
        // Save JWT token
        const token = data.access_token
        setToken(token)

        // Fetch user information
        const userInfo = await authApi.getCurrentUser()

        // Update auth store with user info
        login(userInfo)

        toast({
          title: 'Login successful',
          description: `Welcome back, ${userInfo.username}!`,
        })

        // Call custom callback if provided
        if (onLoginSuccess) {
          onLoginSuccess(userInfo)
        }

        // Handle redirect
        const redirect = searchParams.get('redirect') || redirectPath
        navigate(redirect)
      } catch (error) {
        console.error('Error fetching user info:', error)
        toast({
          variant: 'destructive',
          title: 'Login failed',
          description: 'Error retrieving user information',
        })
      } finally {
        setIsLoading(false)
      }
    },
    onError: (error: any) => {
      console.error('Login error:', error)
      const status = error.response?.status
      
      // Handle 429 (rate limited) status code
      if (status === 429) {
        setIsLockedOut(true)
        setShowWarning(false)
        toast({
          variant: 'destructive',
          title: 'Account locked',
          description: error.response?.data?.detail || 'Too many login attempts. Please try again later.',
        })
      } else {
        setShowWarning(true)
        toast({
          variant: 'destructive',
          title: 'Login failed',
          description: error.response?.data?.detail || 'Incorrect username or password',
        })
      }
      setIsLoading(false)
    },
  })

  const onSubmit = (data: LoginFormValues) => {
    setIsLoading(true)
    loginMutation.mutate(data)
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="w-full max-w-md space-y-8 rounded-lg border bg-card p-8 shadow-sm">
        <div className="text-center">
          <h1 className="text-3xl font-bold">Login</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Sign in to your account to access the platform
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="username">Username</Label>
            <Input
              id="username"
              placeholder="Enter your username"
              {...register('username')}
            />
            {errors.username && (
              <p className="text-sm text-destructive">{errors.username.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              placeholder="Enter your password"
              {...register('password')}
            />
            {errors.password && (
              <p className="text-sm text-destructive">{errors.password.message}</p>
            )}
            {showWarning && !isLockedOut && (
              <p className="text-sm text-amber-600 font-semibold">
                Warning: Multiple failed attempts may lock your account temporarily.
              </p>
            )}
            {isLockedOut && (
              <p className="text-sm text-destructive font-semibold">
                Account temporarily locked. Please try again later.
              </p>
            )}
          </div>

          <Button type="submit" className="w-full" disabled={isLoading || isLockedOut}>
            {isLoading ? 'Logging in...' : isLockedOut ? 'Locked' : 'Login'}
          </Button>
        </form>

        <div className="text-center text-sm">
          <p>
            Don't have an account?{' '}
            <Link to="/register" className="text-primary hover:underline">
              Register now
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default LoginPage
