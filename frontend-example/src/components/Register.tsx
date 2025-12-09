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

import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { useMutation } from '@tanstack/react-query'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { Eye, EyeOff, Check, X } from 'lucide-react'

import { authApi } from '../api/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useToast } from '@/hooks/use-toast'

// Form validation schema
// Use superRefine for password validation to collect all errors at once
const registerSchema = z.object({
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(100, 'Username must be at most 100 characters')
    .regex(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters (a-z, A-Z), numbers (0-9), and underscores (_)'),
  email: z.string()
    .min(1, 'Email is required')
    .email('Please enter a valid email address')
    .max(255, 'Email must be at most 255 characters'),
  password: z.string()
    .min(1, 'Password is required')
    .superRefine((password, ctx) => {
      const errors: string[] = []

      if (password.length < 8) {
        errors.push('be at least 8 characters')
      }
      if (password.length > 128) {
        errors.push('be at most 128 characters')
      }
      if (!/^[a-zA-Z0-9!@#$%^&*]*$/.test(password)) {
        errors.push('only contain letters, numbers, and special characters (!@#$%^&*)')
      }
      if (!/[A-Z]/.test(password)) {
        errors.push('contain at least one uppercase letter')
      }
      if (!/[a-z]/.test(password)) {
        errors.push('contain at least one lowercase letter')
      }
      if (!/[0-9]/.test(password)) {
        errors.push('contain at least one digit')
      }
      if (!/[!@#$%^&*]/.test(password)) {
        errors.push('contain at least one special character (!@#$%^&*)')
      }

      if (errors.length > 0) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: `Password must: ${errors.join('; ')}`,
        })
      }
    }),
  confirmPassword: z.string().min(1, 'Please confirm your password'),
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
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const navigate = useNavigate()
  const { toast } = useToast()

  const {
    register,
    handleSubmit,
    watch,
    trigger,
    formState: { errors },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    mode: 'onChange', // Enable real-time validation
  })

  const password = watch('password', '')
  const confirmPassword = watch('confirmPassword', '')

  // Trigger confirm password validation when password changes
  useEffect(() => {
    if (confirmPassword) {
      trigger('confirmPassword')
    }
  }, [password, trigger, confirmPassword])

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
      const status = error.response?.status
      const data = error.response?.data

      let description = 'An error occurred during registration'
      if (status >= 500) {
        description = 'An internal server error occurred. Please try again later.'
      } else if (!error.response) {
        description = 'Unable to connect to the server. Please check your internet connection.'
      } else if (data?.detail) {
        description = data.detail
      }

      toast({
        variant: 'destructive',
        title: 'Registration failed',
        description: description,
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
            <div className="relative">
              <Input
                id="password"
                type={showPassword ? 'text' : 'password'}
                placeholder="Enter your password"
                {...register('password')}
              />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  <EyeOff className="h-4 w-4 text-muted-foreground" />
                ) : (
                  <Eye className="h-4 w-4 text-muted-foreground" />
                )}
              </Button>
            </div>
            
            {/* Real-time password rules checklist */}
            <div className="space-y-1 rounded-md bg-muted/50 p-3 text-xs">
              <p className="font-medium mb-2">Password must contain:</p>
              <div className="grid grid-cols-1 gap-1 sm:grid-cols-2">
                <div className={`flex items-center gap-2 ${password.length >= 8 && password.length <= 128 ? 'text-green-600' : 'text-muted-foreground'}`}>
                  {password.length >= 8 && password.length <= 128 ? <Check className="h-3 w-3" /> : <div className="h-3 w-3 rounded-full border border-current" />}
                  <span>8-128 characters</span>
                </div>
                <div className={`flex items-center gap-2 ${/[A-Z]/.test(password) ? 'text-green-600' : 'text-muted-foreground'}`}>
                  {/[A-Z]/.test(password) ? <Check className="h-3 w-3" /> : <div className="h-3 w-3 rounded-full border border-current" />}
                  <span>Uppercase letter</span>
                </div>
                <div className={`flex items-center gap-2 ${/[a-z]/.test(password) ? 'text-green-600' : 'text-muted-foreground'}`}>
                  {/[a-z]/.test(password) ? <Check className="h-3 w-3" /> : <div className="h-3 w-3 rounded-full border border-current" />}
                  <span>Lowercase letter</span>
                </div>
                <div className={`flex items-center gap-2 ${/[0-9]/.test(password) ? 'text-green-600' : 'text-muted-foreground'}`}>
                  {/[0-9]/.test(password) ? <Check className="h-3 w-3" /> : <div className="h-3 w-3 rounded-full border border-current" />}
                  <span>Number</span>
                </div>
                <div className={`flex items-center gap-2 ${/[!@#$%^&*]/.test(password) ? 'text-green-600' : 'text-muted-foreground'}`}>
                  {/[!@#$%^&*]/.test(password) ? <Check className="h-3 w-3" /> : <div className="h-3 w-3 rounded-full border border-current" />}
                  <span>Special char (!@#$%^&*)</span>
                </div>
              </div>
            </div>

            {errors.password && (
              <p className="text-sm text-destructive">{errors.password.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="confirmPassword">Confirm Password</Label>
            <div className="relative">
              <Input
                id="confirmPassword"
                type={showConfirmPassword ? 'text' : 'password'}
                placeholder="Confirm your password"
                {...register('confirmPassword')}
              />
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              >
                {showConfirmPassword ? (
                  <EyeOff className="h-4 w-4 text-muted-foreground" />
                ) : (
                  <Eye className="h-4 w-4 text-muted-foreground" />
                )}
              </Button>
            </div>
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
