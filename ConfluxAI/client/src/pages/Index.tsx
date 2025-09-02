
import React, { useState, lazy } from 'react';
import Layout from '@/components/Layout';
import LazyWrapper from '@/components/LazyWrapper';

// Lazy load heavy components
const ChatInterface = lazy(() => import('@/components/ChatInterface'));
const PDFUpload = lazy(() => import('@/components/PDFUpload'));
const ImageUpload = lazy(() => import('@/components/ImageUpload'));
const VideoUpload = lazy(() => import('@/components/VideoUpload'));
const AudioUpload = lazy(() => import('@/components/AudioUpload'));
const DocumentsDashboard = lazy(() => import('@/components/DocumentsDashboard'));

const Index = () => {
  const [activeTab, setActiveTab] = useState('chat');

  const renderContent = () => {
    switch (activeTab) {
      case 'chat':
        return (
          <LazyWrapper skeletonType="chat">
            <ChatInterface />
          </LazyWrapper>
        );
      case 'pdf':
        return (
          <LazyWrapper skeletonType="upload">
            <PDFUpload />
          </LazyWrapper>
        );
      case 'image':
        return (
          <LazyWrapper skeletonType="upload">
            <ImageUpload />
          </LazyWrapper>
        );
      case 'video':
        return (
          <LazyWrapper skeletonType="upload">
            <VideoUpload />
          </LazyWrapper>
        );
      case 'audio':
        return (
          <LazyWrapper skeletonType="upload">
            <AudioUpload />
          </LazyWrapper>
        );
      case 'documents':
        return (
          <LazyWrapper skeletonType="document">
            <DocumentsDashboard />
          </LazyWrapper>
        );
      default:
        return (
          <LazyWrapper skeletonType="chat">
            <ChatInterface />
          </LazyWrapper>
        );
    }
  };

  return (
    <Layout activeTab={activeTab} onTabChange={setActiveTab}>
      <div 
        role="tabpanel" 
        id={`tabpanel-${activeTab}`}
        aria-labelledby={`tab-${activeTab}`}
      >
        {renderContent()}
      </div>
    </Layout>
  );
};

export default Index;
