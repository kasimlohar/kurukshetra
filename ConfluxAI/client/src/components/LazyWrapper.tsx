import React, { Suspense } from 'react';
import { LoadingSkeleton } from './ui/loading-skeleton';

interface LazyWrapperProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  skeletonType?: 'upload' | 'chat' | 'document' | 'card';
}

export const LazyWrapper: React.FC<LazyWrapperProps> = ({ 
  children, 
  fallback,
  skeletonType = 'card' 
}) => {
  const defaultFallback = <LoadingSkeleton type={skeletonType} />;
  
  return (
    <Suspense fallback={fallback || defaultFallback}>
      {children}
    </Suspense>
  );
};

export default LazyWrapper;
