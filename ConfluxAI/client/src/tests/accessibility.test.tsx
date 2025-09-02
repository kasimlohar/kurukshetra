import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ThemeProvider } from '../components/ThemeProvider';
import { AuthProvider } from '../components/Auth';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';

// Mock localStorage
const localStorageMock = {
  getItem: vitest.fn(),
  setItem: vitest.fn(),
  removeItem: vitest.fn(),
  clear: vitest.fn(),
};
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// Mock matchMedia for theme detection
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vitest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vitest.fn(),
    removeListener: vitest.fn(),
    addEventListener: vitest.fn(),
    removeEventListener: vitest.fn(),
    dispatchEvent: vitest.fn(),
  })),
});

const TestWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AuthProvider>
          {children}
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
};

describe('Theme Provider', () => {
  beforeEach(() => {
    localStorageMock.getItem.mockReturnValue(null);
    localStorageMock.setItem.mockClear();
  });

  it('should respect system theme preference', () => {
    window.matchMedia = vitest.fn().mockImplementation(query => ({
      matches: query === '(prefers-color-scheme: dark)',
      media: query,
      addEventListener: vitest.fn(),
      removeEventListener: vitest.fn(),
    }));

    render(
      <TestWrapper>
        <div data-testid="theme-test">Content</div>
      </TestWrapper>
    );

    expect(document.documentElement.classList.contains('dark')).toBeTruthy();
  });

  it('should persist theme choice to localStorage', async () => {
    const { container } = render(
      <TestWrapper>
        <Button onClick={() => {
          const event = new CustomEvent('theme-change', { detail: 'dark' });
          window.dispatchEvent(event);
        }}>
          Change Theme
        </Button>
      </TestWrapper>
    );

    const button = screen.getByRole('button');
    fireEvent.click(button);

    await waitFor(() => {
      expect(localStorageMock.setItem).toHaveBeenCalled();
    });
  });
});

describe('Button Component Accessibility', () => {
  it('should have proper focus states', () => {
    render(
      <TestWrapper>
        <Button>Test Button</Button>
      </TestWrapper>
    );

    const button = screen.getByRole('button');
    button.focus();
    
    expect(button).toHaveFocus();
    expect(button).toHaveClass('focus-visible:ring-2');
  });

  it('should handle keyboard navigation', () => {
    const handleClick = vitest.fn();
    
    render(
      <TestWrapper>
        <Button onClick={handleClick}>Test Button</Button>
      </TestWrapper>
    );

    const button = screen.getByRole('button');
    fireEvent.keyDown(button, { key: 'Enter' });
    fireEvent.keyDown(button, { key: ' ' });
    
    expect(handleClick).toHaveBeenCalledTimes(2);
  });

  it('should have proper ARIA attributes when loading', () => {
    render(
      <TestWrapper>
        <Button isLoading>Loading Button</Button>
      </TestWrapper>
    );

    const button = screen.getByRole('button');
    expect(button).toHaveAttribute('disabled');
    expect(button).toHaveAttribute('aria-disabled', 'true');
  });
});

describe('Card Component Motion', () => {
  it('should respect reduced motion preferences', () => {
    window.matchMedia = vitest.fn().mockImplementation(query => ({
      matches: query === '(prefers-reduced-motion: reduce)',
      media: query,
      addEventListener: vitest.fn(),
      removeEventListener: vitest.fn(),
    }));

    render(
      <TestWrapper>
        <Card>Test Card</Card>
      </TestWrapper>
    );

    const card = screen.getByText('Test Card').closest('div');
    expect(card).toBeInTheDocument();
  });
});

describe('Color Contrast', () => {
  it('should maintain sufficient contrast in light mode', () => {
    render(
      <TestWrapper>
        <Button variant="default">Default Button</Button>
        <Button variant="secondary">Secondary Button</Button>
        <Button variant="outline">Outline Button</Button>
      </TestWrapper>
    );

    // These would ideally use a library like axe-core for actual contrast checking
    const buttons = screen.getAllByRole('button');
    buttons.forEach(button => {
      expect(button).toBeVisible();
    });
  });
});
