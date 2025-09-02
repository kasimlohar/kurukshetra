import { useState, useEffect } from 'react';

export interface TrackedDocument {
  id: string;
  fileName: string;
  fileSize: number;
  fileType: 'pdf' | 'image' | 'video' | 'audio';
  extension: string;
  uploadedAt: string;
  webhookMode: 'test' | 'production';
  status: 'success' | 'processing' | 'failed';
  description?: string;
}

const STORAGE_KEY = 'tracked-documents';

export const useDocumentTracker = () => {
  const [documents, setDocuments] = useState<TrackedDocument[]>([]);

  // Load documents from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setDocuments(parsed);
      } catch (error) {
        console.error('Failed to parse tracked documents:', error);
        setDocuments([]);
      }
    }
  }, []);

  // Save to localStorage whenever documents change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(documents));
  }, [documents]);

  const addDocument = (doc: Omit<TrackedDocument, 'id' | 'uploadedAt'>) => {
    const newDoc: TrackedDocument = {
      ...doc,
      id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
      uploadedAt: new Date().toISOString(),
    };
    setDocuments(prev => [newDoc, ...prev]);
    return newDoc.id;
  };

  const updateDocument = (id: string, updates: Partial<TrackedDocument>) => {
    setDocuments(prev => 
      prev.map(doc => 
        doc.id === id ? { ...doc, ...updates } : doc
      )
    );
  };

  const removeDocument = (id: string) => {
    setDocuments(prev => prev.filter(doc => doc.id !== id));
  };

  const clearAllDocuments = () => {
    setDocuments([]);
    localStorage.removeItem(STORAGE_KEY);
  };

  const getDocumentsByType = (type: TrackedDocument['fileType']) => {
    return documents.filter(doc => doc.fileType === type);
  };

  const getTotalSize = () => {
    return documents.reduce((total, doc) => total + doc.fileSize, 0);
  };

  return {
    documents,
    addDocument,
    updateDocument,
    removeDocument,
    clearAllDocuments,
    getDocumentsByType,
    getTotalSize,
  };
};