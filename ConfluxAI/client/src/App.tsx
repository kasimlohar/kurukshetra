import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Router, Route, Switch } from "wouter";
import { ThemeProvider } from "@/components/ThemeProvider";
import { AuthProvider, ProtectedRoute } from "@/components/Auth";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <ThemeProvider defaultTheme="light" storageKey="task-automator-theme">
      <AuthProvider>
        <TooltipProvider>
          <Toaster />
          <Sonner />
          <Router>
            <Switch>
              <Route path="/" component={() => (
                <ProtectedRoute>
                  <Index />
                </ProtectedRoute>
              )} />
              <Route path="/:rest*" component={NotFound} />
            </Switch>
          </Router>
        </TooltipProvider>
      </AuthProvider>
    </ThemeProvider>
  </QueryClientProvider>
);

export default App;
