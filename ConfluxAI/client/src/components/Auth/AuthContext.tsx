import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface User {
  email: string;
  isAuthenticated: boolean;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, rememberMe?: boolean) => void;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is already authenticated on app load
    const checkAuthStatus = () => {
      try {
        const isAuthenticated = localStorage.getItem('isAuthenticated');
        const userEmail = localStorage.getItem('userEmail');
        
        if (isAuthenticated === 'true' && userEmail) {
          setUser({
            email: userEmail,
            isAuthenticated: true,
          });
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const login = (email: string, rememberMe: boolean = false) => {
    const userData: User = {
      email,
      isAuthenticated: true,
    };

    setUser(userData);
    localStorage.setItem('isAuthenticated', 'true');
    localStorage.setItem('userEmail', email);
    
    if (rememberMe) {
      localStorage.setItem('rememberMe', 'true');
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('rememberMe');
  };

  const value: AuthContextType = {
    user,
    login,
    logout,
    isLoading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
