import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useAuth } from '@/components/Auth';
import { User, Shield, CheckCircle, Clock, Mail, Settings } from 'lucide-react';
import { toast } from '@/hooks/use-toast';

const AuthDemo: React.FC = () => {
  const { user, logout } = useAuth();
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    
    // Simulate logout delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    logout();
    toast({
      title: "Logged out successfully",
      description: "You have been logged out of your account.",
    });
    
    setIsLoggingOut(false);
  };

  const handleTestAction = () => {
    toast({
      title: "Protected Action",
      description: "This action is only available to authenticated users!",
    });
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="w-16 h-16 mx-auto bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
          <Shield className="w-8 h-8 text-white" />
        </div>
        <div>
          <h1 className="text-3xl font-bold gradient-text">Authentication Demo</h1>
          <p className="text-muted-foreground mt-2">
            Experience the modern authentication system with advanced features
          </p>
        </div>
      </div>

      {/* User Status Card */}
      <Card className="border-green-200 bg-green-50 dark:bg-green-900/20 dark:border-green-800">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-green-700 dark:text-green-400">
            <CheckCircle className="w-5 h-5" />
            Authentication Status
          </CardTitle>
          <CardDescription>
            You are successfully authenticated and can access protected content
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <User className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="font-medium">{user?.email?.split('@')[0] || 'User'}</p>
                <p className="text-sm text-muted-foreground">{user?.email}</p>
              </div>
            </div>
            <Badge variant="default" className="bg-green-500 hover:bg-green-600">
              Online
            </Badge>
          </div>
          
          <div className="flex gap-2 pt-2">
            <Button 
              variant="outline" 
              size="sm"
              onClick={handleTestAction}
              className="flex-1"
            >
              <Settings className="w-4 h-4 mr-2" />
              Test Protected Action
            </Button>
            <Button 
              variant="destructive" 
              size="sm"
              onClick={handleLogout}
              disabled={isLoggingOut}
              className="flex-1"
            >
              {isLoggingOut ? (
                <Clock className="w-4 h-4 mr-2 animate-spin" />
              ) : (
                <Mail className="w-4 h-4 mr-2" />
              )}
              {isLoggingOut ? 'Logging out...' : 'Logout'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Features Showcase */}
      <div className="grid md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>🎨 Design Features</CardTitle>
            <CardDescription>Modern UI with glassmorphism effects</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span className="text-sm">Responsive design (mobile & desktop)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <span className="text-sm">Dark/light theme support</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span className="text-sm">Smooth animations & transitions</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <span className="text-sm">Glassmorphism backdrop effects</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span className="text-sm">Gradient backgrounds & text</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>🔒 Security Features</CardTitle>
            <CardDescription>Advanced authentication capabilities</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm">Real-time form validation</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-emerald-500 rounded-full"></div>
                <span className="text-sm">Password strength indicator</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm">Email format validation</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-emerald-500 rounded-full"></div>
                <span className="text-sm">Remember me functionality</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm">Persistent authentication state</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>🚀 User Experience</CardTitle>
            <CardDescription>Seamless authentication flow</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                <span className="text-sm">Toggle between login/signup</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                <span className="text-sm">Loading states & spinners</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                <span className="text-sm">Toast notifications</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                <span className="text-sm">Password visibility toggle</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                <span className="text-sm">Accessible form elements</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>⚡ Technical Stack</CardTitle>
            <CardDescription>Built with modern technologies</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-cyan-500 rounded-full"></div>
                <span className="text-sm">React with TypeScript</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span className="text-sm">Tailwind CSS styling</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-cyan-500 rounded-full"></div>
                <span className="text-sm">Lucide React icons</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span className="text-sm">shadcn/ui components</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-cyan-500 rounded-full"></div>
                <span className="text-sm">Context API state management</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Integration Info */}
      <Card className="border-blue-200 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-800">
        <CardHeader>
          <CardTitle className="text-blue-700 dark:text-blue-400">
            🎉 Ready for Production
          </CardTitle>
          <CardDescription>
            The authentication system is fully integrated and production-ready
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <p className="text-sm">
              ✅ <strong>AuthProvider</strong> wraps your entire application<br />
              ✅ <strong>ProtectedRoute</strong> guards your protected pages<br />
              ✅ <strong>User menu</strong> integrated in the header<br />
              ✅ <strong>Persistent sessions</strong> across page refreshes<br />
              ✅ <strong>Mobile responsive</strong> design implemented
            </p>
            <div className="pt-2">
              <Badge variant="outline" className="text-blue-600 border-blue-300">
                🚀 All features working and tested
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AuthDemo;
