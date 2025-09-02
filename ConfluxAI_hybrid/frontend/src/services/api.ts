import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with default configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth tokens, logging, etc.
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Log requests in development
    if (import.meta.env.DEV) {
      console.log('API Request:', config.method?.toUpperCase(), config.url, config.data);
    }
    
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors globally
apiClient.interceptors.response.use(
  (response) => {
    // Log responses in development
    if (import.meta.env.DEV) {
      console.log('API Response:', response.status, response.config.url, response.data);
    }
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data || error.message);
    
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Unauthorized - clear auth and redirect to login
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

// Type definitions
export interface SearchRequest {
  query: string;
  limit?: number;
  threshold?: number;
  file_filters?: string[];
  search_type?: 'semantic' | 'hybrid' | 'keyword';
}

export interface SearchResult {
  id: string;
  filename: string;
  content: string;
  score: number;
  metadata?: Record<string, any>;
}

export interface SearchResponse {
  results: SearchResult[];
  total_results: number;
  search_time: number;
  query_analysis: Record<string, any>;
}

export interface SummaryRequest {
  text?: string;
  document_id?: string;
  max_length?: number;
  summary_type?: string;
}

export interface SummaryResponse {
  summary: string;
  key_points: string[];
  confidence: number;
  original_length: number;
  summary_length: number;
  compression_ratio: number;
  processing_time: number;
}

export interface QuestionRequest {
  question: string;
  context_limit?: number;
  file_filters?: string[];
  session_id?: string;
}

export interface QuestionResponse {
  answer: string;
  confidence: number;
  sources: SearchResult[];
  processing_time: number;
  session_id?: string;
  follow_up_suggestions?: string[];
}

export interface DocumentUploadRequest {
  files: File[];
  processing_options?: Record<string, any>;
}

export interface UploadResponse {
  task_id: string;
  files_processed: number;
  estimated_time: number;
}

export interface HealthResponse {
  status: string;
  version: string;
  services: Record<string, any>;
  uptime: number;
}

export interface AnalyticsResponse {
  search_analytics: Record<string, any>;
  ai_analytics: Record<string, any>;
  system_performance: Record<string, any>;
  user_activity: Record<string, any>;
}

// API Service Class
class APIService {
  // Search endpoints
  async search(request: SearchRequest): Promise<SearchResponse> {
    const response = await apiClient.post<SearchResponse>('/search/', request);
    return response.data;
  }

  async hybridSearch(request: SearchRequest): Promise<SearchResponse> {
    const response = await apiClient.post<SearchResponse>('/search/hybrid', request);
    return response.data;
  }

  async searchSuggestions(query: string): Promise<string[]> {
    const response = await apiClient.get<string[]>(`/search/suggestions?q=${encodeURIComponent(query)}`);
    return response.data;
  }

  // AI endpoints
  async summarizeText(request: SummaryRequest): Promise<SummaryResponse> {
    const response = await apiClient.post<SummaryResponse>('/ai/summarize', request);
    return response.data;
  }

  async askQuestion(request: QuestionRequest): Promise<QuestionResponse> {
    const response = await apiClient.post<QuestionResponse>('/ai/question', request);
    return response.data;
  }

  async getConversationHistory(sessionId: string): Promise<any[]> {
    const response = await apiClient.get(`/ai/conversation/${sessionId}`);
    return response.data;
  }

  async clearConversation(sessionId: string): Promise<void> {
    await apiClient.delete(`/ai/conversation/${sessionId}`);
  }

  // Document management
  async uploadDocuments(request: DocumentUploadRequest): Promise<UploadResponse> {
    const formData = new FormData();
    
    request.files.forEach((file, index) => {
      formData.append(`files`, file);
    });

    if (request.processing_options) {
      formData.append('processing_options', JSON.stringify(request.processing_options));
    }

    const response = await apiClient.post<UploadResponse>('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  }

  async getDocument(documentId: string): Promise<any> {
    const response = await apiClient.get(`/documents/${documentId}`);
    return response.data;
  }

  async deleteDocument(documentId: string): Promise<void> {
    await apiClient.delete(`/documents/${documentId}`);
  }

  async getDocumentList(page = 1, limit = 20): Promise<any> {
    const response = await apiClient.get(`/documents?page=${page}&limit=${limit}`);
    return response.data;
  }

  // System endpoints
  async getHealth(): Promise<HealthResponse> {
    const response = await apiClient.get<HealthResponse>('/health');
    return response.data;
  }

  async getAnalytics(): Promise<AnalyticsResponse> {
    const response = await apiClient.get<AnalyticsResponse>('/analytics');
    return response.data;
  }

  async getSystemStatus(): Promise<any> {
    const response = await apiClient.get('/status');
    return response.data;
  }

  // Task management
  async getTaskStatus(taskId: string): Promise<any> {
    const response = await apiClient.get(`/tasks/${taskId}`);
    return response.data;
  }

  async cancelTask(taskId: string): Promise<void> {
    await apiClient.post(`/tasks/${taskId}/cancel`);
  }

  async getActiveTasks(): Promise<any[]> {
    const response = await apiClient.get('/tasks/active');
    return response.data;
  }

  // Knowledge graph endpoints
  async getKnowledgeGraph(entity?: string): Promise<any> {
    const url = entity ? `/knowledge-graph?entity=${encodeURIComponent(entity)}` : '/knowledge-graph';
    const response = await apiClient.get(url);
    return response.data;
  }

  async searchKnowledgeGraph(query: string): Promise<any> {
    const response = await apiClient.post('/knowledge-graph/search', { query });
    return response.data;
  }

  // Settings and configuration
  async getSettings(): Promise<any> {
    const response = await apiClient.get('/settings');
    return response.data;
  }

  async updateSettings(settings: Record<string, any>): Promise<any> {
    const response = await apiClient.put('/settings', settings);
    return response.data;
  }

  // Utility methods
  async exportData(format: 'json' | 'csv' = 'json'): Promise<Blob> {
    const response = await apiClient.get(`/export?format=${format}`, {
      responseType: 'blob',
    });
    return response.data;
  }

  async importData(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await apiClient.post('/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  }

  // Custom request method for special cases
  async customRequest<T = any>(config: AxiosRequestConfig): Promise<T> {
    const response = await apiClient.request<T>(config);
    return response.data;
  }
}

// Create and export singleton instance
export const apiService = new APIService();
export default apiService;

// Export axios instance for direct use if needed
export { apiClient };
