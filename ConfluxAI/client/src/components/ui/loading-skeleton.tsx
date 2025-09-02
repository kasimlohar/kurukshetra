import React from 'react';
import { motion } from 'framer-motion';
import { Skeleton } from './skeleton';

interface LoadingSkeletonProps {
  type?: 'upload' | 'chat' | 'document' | 'card';
  className?: string;
}

export const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({ 
  type = 'card', 
  className = '' 
}) => {
  const renderUploadSkeleton = () => (
    <div className={`space-y-6 p-6 ${className}`}>
      <div className="space-y-2">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-4 w-72" />
      </div>
      
      <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-8">
        <div className="flex flex-col items-center space-y-4">
          <Skeleton className="h-12 w-12 rounded-full" />
          <Skeleton className="h-6 w-40" />
          <Skeleton className="h-4 w-56" />
          <Skeleton className="h-10 w-32" />
        </div>
      </div>
      
      <div className="space-y-3">
        <Skeleton className="h-5 w-32" />
        <div className="grid grid-cols-2 gap-4">
          <Skeleton className="h-20 w-full" />
          <Skeleton className="h-20 w-full" />
        </div>
      </div>
    </div>
  );

  const renderChatSkeleton = () => (
    <div className={`space-y-4 p-6 ${className}`}>
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="flex gap-3">
            <Skeleton className="h-8 w-8 rounded-full" />
            <div className="space-y-2 flex-1">
              <Skeleton className="h-4 w-20" />
              <Skeleton className="h-16 w-full max-w-md" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderDocumentSkeleton = () => (
    <div className={`space-y-6 p-6 ${className}`}>
      <div className="flex justify-between items-center">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-10 w-24" />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} className="border rounded-lg p-4 space-y-3">
            <Skeleton className="h-32 w-full" />
            <Skeleton className="h-5 w-full" />
            <Skeleton className="h-4 w-20" />
            <div className="flex justify-between">
              <Skeleton className="h-6 w-16" />
              <Skeleton className="h-6 w-6" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderCardSkeleton = () => (
    <div className={`border rounded-lg p-6 space-y-4 ${className}`}>
      <div className="space-y-2">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-4 w-48" />
      </div>
      <Skeleton className="h-32 w-full" />
      <div className="flex justify-between">
        <Skeleton className="h-8 w-20" />
        <Skeleton className="h-8 w-20" />
      </div>
    </div>
  );

  const skeletons = {
    upload: renderUploadSkeleton,
    chat: renderChatSkeleton,
    document: renderDocumentSkeleton,
    card: renderCardSkeleton,
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
      role="status"
      aria-label="Loading content"
    >
      {skeletons[type]()}
    </motion.div>
  );
};

export default LoadingSkeleton;
