import React from 'react';
import { useAuth } from './AuthContext';
import LoginSignup from './LoginSignup';
import { Loader2 } from 'lucide-react';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { user, isLoading } = useAuth();

  // Show loading spinner while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  // Show login page if user is not authenticated
  if (!user?.isAuthenticated) {
    return <LoginSignup />;
  }

  // Show protected content if user is authenticated
  return <>{children}</>;
};

export default ProtectedRoute;
