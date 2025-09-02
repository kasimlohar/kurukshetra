import React, { useState, useEffect } from 'react';
import { Eye, EyeOff, Mail, Lock, User, Loader2, CheckCircle, XCircle, Shield } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { toast } from '@/hooks/use-toast';
import { useAuth } from './AuthContext';
import Spline from '@splinetool/react-spline';

interface FormData {
  email: string;
  password: string;
  confirmPassword?: string;
}

interface FormErrors {
  email?: string;
  password?: string;
  confirmPassword?: string;
}

interface PasswordStrength {
  score: number;
  feedback: string[];
}

const LoginSignup: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState<PasswordStrength>({ score: 0, feedback: [] });
  
  const { login, user } = useAuth();

  // Password strength calculator
  const calculatePasswordStrength = (password: string): PasswordStrength => {
    let score = 0;
    const feedback: string[] = [];

    if (password.length === 0) {
      return { score: 0, feedback: [] };
    }

    // Length check
    if (password.length >= 8) {
      score += 25;
    } else {
      feedback.push('At least 8 characters');
    }

    // Uppercase check
    if (/[A-Z]/.test(password)) {
      score += 25;
    } else {
      feedback.push('One uppercase letter');
    }

    // Lowercase check
    if (/[a-z]/.test(password)) {
      score += 25;
    } else {
      feedback.push('One lowercase letter');
    }

    // Number or symbol check
    if (/[\d\W]/.test(password)) {
      score += 25;
    } else {
      feedback.push('One number or symbol');
    }

    return { score, feedback };
  };

  // Email validation
  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  // Form validation
  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (!isLogin && formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters long';
    }

    // Confirm password validation (signup only)
    if (!isLogin) {
      if (!formData.confirmPassword) {
        newErrors.confirmPassword = 'Please confirm your password';
      } else if (formData.password !== formData.confirmPassword) {
        newErrors.confirmPassword = 'Passwords do not match';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));

    // Clear errors when user starts typing
    if (errors[name as keyof FormErrors]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }

    // Calculate password strength for signup
    if (name === 'password' && !isLogin) {
      setPasswordStrength(calculatePasswordStrength(value));
    }
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Use the login function from AuthContext
      login(formData.email, rememberMe);

      toast({
        title: isLogin ? "Welcome back!" : "Account created successfully!",
        description: isLogin 
          ? "You have been logged in successfully." 
          : "Please check your email to verify your account.",
      });

      // No need to manually redirect, ProtectedRoute will handle it

    } catch (error) {
      toast({
        title: "Authentication failed",
        description: "Please check your credentials and try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Toggle between login and signup
  const toggleMode = () => {
    setIsLogin(!isLogin);
    setFormData({ email: '', password: '', confirmPassword: '' });
    setErrors({});
    setPasswordStrength({ score: 0, feedback: [] });
  };

  // Password strength color
  const getPasswordStrengthColor = (score: number) => {
    if (score <= 25) return 'bg-red-500';
    if (score <= 50) return 'bg-orange-500';
    if (score <= 75) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  // Password strength text
  const getPasswordStrengthText = (score: number) => {
    if (score <= 25) return 'Weak';
    if (score <= 50) return 'Fair';
    if (score <= 75) return 'Good';
    return 'Strong';
  };

  useEffect(() => {
    // If user is already authenticated, no need to show login page
    // The ProtectedRoute component will handle redirecting
    if (user?.isAuthenticated) {
      return;
    }
  }, [user]);

  return (
    <div className="min-h-screen flex flex-col lg:flex-row bg-gradient-to-br from-blue-50 via-purple-50 to-blue-50 dark:from-slate-900 dark:via-purple-900/20 dark:to-slate-900">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full opacity-20 blur-3xl animate-pulse" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-r from-purple-400 to-blue-500 rounded-full opacity-20 blur-3xl animate-pulse" />
      </div>

      {/* Left side - Login Card */}
      <div className="flex-1 flex items-center justify-center p-4 relative z-10 min-h-screen lg:min-h-0">
        <div className="w-full max-w-md">
          <Card className="glass glass-dark border-white/20 shadow-2xl backdrop-blur-xl animate-scale-in bg-white/90 dark:bg-slate-900/90">
          <CardHeader className="text-center space-y-4">
            {/* Logo/Icon */}
            <div className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center animate-fade-in">
              <Shield className="w-8 h-8 text-white" />
            </div>
            
            <div className="space-y-2 animate-slide-in">
              <CardTitle className="text-2xl font-bold gradient-text">
                {isLogin ? 'Welcome Back' : 'Create Account'}
              </CardTitle>
              <CardDescription className="text-muted-foreground">
                {isLogin 
                  ? 'Sign in to your account to continue' 
                  : 'Join us to start automating your tasks'
                }
              </CardDescription>
            </div>
          </CardHeader>

          <CardContent className="space-y-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Email Field */}
              <div className="space-y-2">
                <Label htmlFor="email" className="text-sm font-medium">
                  Email Address
                </Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    placeholder="Enter your email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className={`pl-10 transition-all duration-200 ${
                      errors.email 
                        ? 'border-red-500 focus:ring-red-500' 
                        : formData.email && validateEmail(formData.email)
                        ? 'border-green-500 focus:ring-green-500'
                        : ''
                    }`}
                    aria-describedby={errors.email ? "email-error" : undefined}
                  />
                  {formData.email && validateEmail(formData.email) && (
                    <CheckCircle className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-green-500" />
                  )}
                  {errors.email && (
                    <XCircle className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-red-500" />
                  )}
                </div>
                {errors.email && (
                  <p id="email-error" className="text-sm text-red-500 animate-fade-in">
                    {errors.email}
                  </p>
                )}
              </div>

              {/* Password Field */}
              <div className="space-y-2">
                <Label htmlFor="password" className="text-sm font-medium">
                  Password
                </Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    placeholder="Enter your password"
                    value={formData.password}
                    onChange={handleInputChange}
                    className={`pl-10 pr-10 transition-all duration-200 ${
                      errors.password ? 'border-red-500 focus:ring-red-500' : ''
                    }`}
                    aria-describedby={errors.password ? "password-error" : undefined}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
                {errors.password && (
                  <p id="password-error" className="text-sm text-red-500 animate-fade-in">
                    {errors.password}
                  </p>
                )}
                
                {/* Password Strength Indicator (Signup only) */}
                {!isLogin && formData.password && (
                  <div className="space-y-2 animate-fade-in">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-muted-foreground">Password strength:</span>
                      <span className={`font-medium ${
                        passwordStrength.score <= 25 ? 'text-red-500' :
                        passwordStrength.score <= 50 ? 'text-orange-500' :
                        passwordStrength.score <= 75 ? 'text-yellow-500' :
                        'text-green-500'
                      }`}>
                        {getPasswordStrengthText(passwordStrength.score)}
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700">
                      <div 
                        className={`h-2 rounded-full transition-all duration-300 ${getPasswordStrengthColor(passwordStrength.score)}`}
                        style={{ width: `${passwordStrength.score}%` }}
                      />
                    </div>
                    {passwordStrength.feedback.length > 0 && (
                      <ul className="text-xs text-muted-foreground space-y-1">
                        {passwordStrength.feedback.map((item, index) => (
                          <li key={index} className="flex items-center gap-2">
                            <div className="w-1 h-1 bg-muted-foreground rounded-full" />
                            {item}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </div>

              {/* Confirm Password Field (Signup only) */}
              {!isLogin && (
                <div className="space-y-2 animate-fade-in">
                  <Label htmlFor="confirmPassword" className="text-sm font-medium">
                    Confirm Password
                  </Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <Input
                      id="confirmPassword"
                      name="confirmPassword"
                      type={showConfirmPassword ? 'text' : 'password'}
                      placeholder="Confirm your password"
                      value={formData.confirmPassword || ''}
                      onChange={handleInputChange}
                      className={`pl-10 pr-10 transition-all duration-200 ${
                        errors.confirmPassword 
                          ? 'border-red-500 focus:ring-red-500'
                          : formData.confirmPassword && formData.password === formData.confirmPassword
                          ? 'border-green-500 focus:ring-green-500'
                          : ''
                      }`}
                      aria-describedby={errors.confirmPassword ? "confirm-password-error" : undefined}
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                      aria-label={showConfirmPassword ? "Hide password" : "Show password"}
                    >
                      {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                    {formData.confirmPassword && formData.password === formData.confirmPassword && (
                      <CheckCircle className="absolute right-10 top-1/2 transform -translate-y-1/2 w-4 h-4 text-green-500" />
                    )}
                  </div>
                  {errors.confirmPassword && (
                    <p id="confirm-password-error" className="text-sm text-red-500 animate-fade-in">
                      {errors.confirmPassword}
                    </p>
                  )}
                </div>
              )}

              {/* Remember Me & Forgot Password (Login only) */}
              {isLogin && (
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="remember"
                      checked={rememberMe}
                      onCheckedChange={(checked) => setRememberMe(checked as boolean)}
                    />
                    <Label 
                      htmlFor="remember" 
                      className="text-sm font-normal cursor-pointer"
                    >
                      Remember me
                    </Label>
                  </div>
                  <button
                    type="button"
                    className="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 transition-colors"
                    onClick={() => {
                      toast({
                        title: "Password Reset",
                        description: "Password reset functionality will be available soon.",
                      });
                    }}
                  >
                    Forgot password?
                  </button>
                </div>
              )}

              {/* Submit Button */}
              <Button
                type="submit"
                className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-medium py-2.5 transition-all duration-200 transform hover:scale-[1.02] disabled:transform-none"
                disabled={isLoading}
              >
                {isLoading ? (
                  <div className="flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    {isLogin ? 'Signing in...' : 'Creating account...'}
                  </div>
                ) : (
                  isLogin ? 'Sign In' : 'Create Account'
                )}
              </Button>
            </form>

            {/* Toggle Mode */}
            <div className="text-center pt-4 border-t border-border">
              <p className="text-sm text-muted-foreground">
                {isLogin ? "Don't have an account?" : "Already have an account?"}
                <button
                  type="button"
                  onClick={toggleMode}
                  className="ml-2 text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 font-medium transition-colors"
                >
                  {isLogin ? 'Sign up' : 'Sign in'}
                </button>
              </p>
            </div>

            {/* Terms (Signup only) */}
            {!isLogin && (
              <p className="text-xs text-muted-foreground text-center leading-relaxed animate-fade-in">
                By creating an account, you agree to our{' '}
                <a href="#" className="text-blue-600 hover:text-blue-700 dark:text-blue-400 transition-colors">
                  Terms of Service
                </a>{' '}
                and{' '}
                <a href="#" className="text-blue-600 hover:text-blue-700 dark:text-blue-400 transition-colors">
                  Privacy Policy
                </a>
              </p>
            )}
          </CardContent>
        </Card>
        </div>
      </div>

      {/* Right side - 3D Spline Component */}
      <div className="hidden lg:flex flex-1 items-center justify-center relative overflow-hidden min-h-screen">
        <div className="w-full h-full">
          <Spline 
            scene="https://prod.spline.design/aOlcecFdfZC0nLtw/scene.splinecode"
            className="w-full h-full"
          />
        </div>
      </div>
    </div>
  );
};

export default LoginSignup;
