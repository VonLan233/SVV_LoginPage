import { useAuthStore } from '../store/auth'
import { useNavigate } from 'react-router-dom'
import { Button } from '../components/ui/button'

export default function Dashboard() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-card rounded-lg shadow-sm p-8">
            <div className="flex items-center justify-between mb-8">
              <h1 className="text-3xl font-bold">Dashboard</h1>
              <Button onClick={handleLogout} variant="outline">
                Logout
              </Button>
            </div>

            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-semibold mb-4">Welcome back!</h2>
                <div className="bg-muted rounded-lg p-6 space-y-3">
                  <div className="flex items-center gap-2">
                    <span className="font-medium">Username:</span>
                    <span className="text-muted-foreground">{user?.username}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="font-medium">Email:</span>
                    <span className="text-muted-foreground">{user?.email}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="font-medium">User ID:</span>
                    <span className="text-muted-foreground">{user?.id}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="font-medium">Status:</span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Active
                    </span>
                  </div>
                </div>
              </div>

              <div className="border-t pt-6">
                <h3 className="text-lg font-semibold mb-3">About SVV-LoginPage</h3>
                <div className="prose prose-sm max-w-none text-muted-foreground">
                  <p>
                    This is a demonstration of the SVV-LoginPage authentication module.
                    You've successfully logged in and your session is being managed with JWT tokens.
                  </p>
                  <ul className="mt-3 space-y-2">
                    <li>✅ User authentication with JWT</li>
                    <li>✅ Secure password hashing (bcrypt)</li>
                    <li>✅ State management with Zustand</li>
                    <li>✅ Persistent localStorage session</li>
                    <li>✅ Protected routes</li>
                  </ul>
                </div>
              </div>

              <div className="border-t pt-6">
                <h3 className="text-lg font-semibold mb-3">API Info</h3>
                <div className="bg-muted rounded-lg p-4">
                  <p className="text-sm font-mono text-muted-foreground">
                    Backend API: http://localhost:8000
                  </p>
                  <p className="text-sm font-mono text-muted-foreground mt-2">
                    API Docs: http://localhost:8000/docs
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
