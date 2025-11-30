/**
 * SVV-LoginPage Register Component
 *
 * A complete registration form with React Hook Form validation,
 * email validation, and password confirmation.
 *
 * Features:
 * - Form validation with Zod schema
 * - Email format validation
 * - Password confirmation matching
 * - Toast notifications for feedback
 * - Redirect to login after successful registration
 *
 * Dependencies:
 * - react-hook-form: Form management
 * - zod: Schema validation
 * - @tanstack/react-query: API state management
 * - react-router-dom: Navigation
 * - shadcn/ui: UI components (Button, Input, Label)
 */

import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { useMutation } from '@tanstack/react-query'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'

import { authApi } from '../api/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useToast } from '@/hooks/use-toast'

// Form validation schema
const registerSchema = z.object({
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(50, 'Username must be at most 50 characters')
    .regex(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters (a-z, A-Z), numbers (0-9), and underscores (_)'),
  email: z.string().email('Please enter a valid email address'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .max(128, 'Password must be at most 128 characters')
    .regex(/^[a-zA-Z0-9!@#$%^&*]+$/, 'Password contains illegal characters. Only letters (a-z, A-Z), numbers (0-9), and special characters (!@#$%^&*) are allowed')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least one digit')
    .regex(/[!@#$%^&*]/, 'Password must contain at least one special character (!@#$%^&*)'),
  confirmPassword: z.string().min(8, 'Password must be at least 8 characters'),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
})

type RegisterFormValues = z.infer<typeof registerSchema>

interface RegisterPageProps {
  /** Optional custom redirect path after successful registration */
  redirectPath?: string
  /** Optional callback after successful registration */
  onRegisterSuccess?: () => void
}

const RegisterPage = ({ redirectPath = '/login', onRegisterSuccess }: RegisterPageProps) => {
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()
  const { toast } = useToast()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
  })

  const registerMutation = useMutation({
    mutationFn: (data: Omit<RegisterFormValues, 'confirmPassword'>) => {
      return authApi.register({
        username: data.username,
        email: data.email,
        password: data.password,
      })
    },
    onSuccess: () => {
      setIsLoading(false)
      
      toast({
        title: 'Registration successful',
        description: 'You have successfully registered. Please login.',
      })

      // Call custom callback if provided
      if (onRegisterSuccess) {
        onRegisterSuccess()
      }

      navigate(redirectPath)
    },
    onError: (error: any) => {
      console.error('Registration error:', error)
      toast({
        variant: 'destructive',
        title: 'Registration failed',
        description: error.response?.data?.detail || 'An error occurred during registration',
      })
      setIsLoading(false)
    },
  })

  const onSubmit = (data: RegisterFormValues) => {
    setIsLoading(true)
    const { confirmPassword, ...registerData } = data
    registerMutation.mutate(registerData)
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="w-full max-w-md space-y-8 rounded-lg border bg-card p-8 shadow-sm">
        <div className="text-center">
          <h1 className="text-3xl font-bold">Register</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Create a new account to access the platform
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
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="Enter your email"
              {...register('email')}
            />
            {errors.email && (
              <p className="text-sm text-destructive">{errors.email.message}</p>
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
            <p className="text-xs text-muted-foreground">
              Only letters (a-z, A-Z), numbers (0-9), and special characters (!@#$%^&*) are allowed
            </p>
            {errors.password && (
              <p className="text-sm text-destructive">{errors.password.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="confirmPassword">Confirm Password</Label>
            <Input
              id="confirmPassword"
              type="password"
              placeholder="Confirm your password"
              {...register('confirmPassword')}
            />
            {errors.confirmPassword && (
              <p className="text-sm text-destructive">{errors.confirmPassword.message}</p>
            )}
          </div>

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? 'Registering...' : 'Register'}
          </Button>
        </form>

        <div className="text-center text-sm">
          <p>
            Already have an account?{' '}
            <Link to="/login" className="text-primary hover:underline">
              Login
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default RegisterPage
