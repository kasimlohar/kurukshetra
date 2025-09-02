// WebSocket Events
export interface WebSocketEvents {
  // Search events
  'search_progress': (data: { progress: number; stage: string; results?: any[] }) => void;
  'search_complete': (data: { results: any[]; total_time: number }) => void;
  'search_error': (data: { error: string }) => void;

  // AI processing events
  'ai_progress': (data: { progress: number; stage: string; task_id: string }) => void;
  'ai_complete': (data: { result: any; task_id: string }) => void;
  'ai_error': (data: { error: string; task_id: string }) => void;

  // Document processing events
  'upload_progress': (data: { progress: number; filename: string; task_id: string }) => void;
  'upload_complete': (data: { filename: string; document_id: string; task_id: string }) => void;
  'upload_error': (data: { error: string; filename: string; task_id: string }) => void;

  // System events
  'system_status': (data: { status: string; services: Record<string, any> }) => void;
  'system_notification': (data: { type: 'info' | 'warning' | 'error'; message: string }) => void;

  // Real-time analytics
  'analytics_update': (data: { metrics: Record<string, any>; timestamp: string }) => void;
  'user_activity': (data: { activity: string; user_id?: string; timestamp: string }) => void;

  // Connection events
  'connection': (data: { status: string; [key: string]: any }) => void;
}

// WebSocket Service Class
class WebSocketService {
  private socket: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000; // Start with 1 second
  private isConnected = false;
  private eventListeners: Map<string, Set<Function>> = new Map();
  private reconnectTimer: number | null = null;

  constructor() {
    this.initialize();
  }

  private initialize() {
    const wsUrl = (window as any).ENV?.VITE_WS_URL || 'ws://localhost:8000/ws';
    
    try {
      this.socket = new WebSocket(wsUrl);
      this.setupEventListeners();
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
      this.scheduleReconnect();
    }
  }

  private setupEventListeners() {
    if (!this.socket) return;

    this.socket.onopen = () => {
      console.log('WebSocket connected');
      this.isConnected = true;
      this.reconnectAttempts = 0;
      this.reconnectDelay = 1000; // Reset delay
      
      if (this.reconnectTimer) {
        clearTimeout(this.reconnectTimer);
        this.reconnectTimer = null;
      }
      
      // Emit connection event to subscribers
      this.emit('connection', { status: 'connected' });
    };

    this.socket.onclose = () => {
      console.log('WebSocket disconnected');
      this.isConnected = false;
      
      // Emit disconnection event to subscribers
      this.emit('connection', { status: 'disconnected' });
      
      // Try to reconnect
      this.scheduleReconnect();
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
      
      if (!this.isConnected) {
        this.scheduleReconnect();
      }
    };

    this.socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        const eventType = message.type;
        const data = message.data;
        
        // Emit the event to registered listeners
        this.emit(eventType, data);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };
  }

  private scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      this.emit('connection', { status: 'failed', error: 'Max reconnection attempts reached' });
      return;
    }

    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }

    this.reconnectTimer = window.setTimeout(() => {
      this.reconnectAttempts++;
      this.reconnectDelay = Math.min(this.reconnectDelay * 2, 30000); // Max 30 seconds
      console.log(`Reconnection attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts} in ${this.reconnectDelay}ms`);
      
      this.initialize();
    }, this.reconnectDelay);
  }

  // Subscribe to events
  on<K extends keyof WebSocketEvents>(event: K, callback: WebSocketEvents[K]): () => void;
  on(event: string, callback: Function): () => void;
  on(event: string, callback: Function): () => void {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, new Set());
    }
    
    this.eventListeners.get(event)!.add(callback);
    
    // Return unsubscribe function
    return () => {
      const listeners = this.eventListeners.get(event);
      if (listeners) {
        listeners.delete(callback);
        if (listeners.size === 0) {
          this.eventListeners.delete(event);
        }
      }
    };
  }

  // Emit events to registered listeners
  private emit(event: string, ...args: any[]) {
    const listeners = this.eventListeners.get(event);
    if (listeners) {
      listeners.forEach((callback) => {
        try {
          callback(...args);
        } catch (error) {
          console.error(`Error in WebSocket event listener for ${event}:`, error);
        }
      });
    }
  }

  // Send messages to server
  sendMessage(type: string, data?: any) {
    if (this.socket && this.isConnected && this.socket.readyState === WebSocket.OPEN) {
      const message = JSON.stringify({ type, data });
      this.socket.send(message);
    } else {
      console.warn('WebSocket not connected. Cannot send message:', type);
    }
  }

  // Real-time search with progress updates
  startLiveSearch(query: string, options?: any) {
    this.sendMessage('live_search', { query, ...options });
  }

  // Subscribe to AI processing updates
  subscribeToAIProgress(taskId: string) {
    this.sendMessage('subscribe', { subscription: 'ai_progress', task_id: taskId });
  }

  // Subscribe to document upload progress
  subscribeToUploadProgress(taskId: string) {
    this.sendMessage('subscribe', { subscription: 'upload_progress', task_id: taskId });
  }

  // Subscribe to system status updates
  subscribeToSystemStatus() {
    this.sendMessage('subscribe', { subscription: 'system_events' });
  }

  // Subscribe to real-time analytics
  subscribeToAnalytics() {
    this.sendMessage('subscribe', { subscription: 'analytics' });
  }

  // Unsubscribe from updates
  unsubscribe(subscription: string, id?: string) {
    this.sendMessage('unsubscribe', { subscription, id });
  }

  // Get connection status
  getConnectionStatus() {
    return {
      connected: this.isConnected,
      socket_url: this.socket?.url,
      ready_state: this.socket?.readyState,
      reconnect_attempts: this.reconnectAttempts,
    };
  }

  // Manually reconnect
  reconnect() {
    if (this.socket) {
      this.socket.close();
    }
    this.initialize();
  }

  // Disconnect
  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.isConnected = false;
    }
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
  }

  // Cleanup
  destroy() {
    this.eventListeners.clear();
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
  }
}

// Create singleton instance
let webSocketService: WebSocketService | null = null;

export const initializeWebSocket = (): WebSocketService => {
  if (!webSocketService) {
    webSocketService = new WebSocketService();
  }
  return webSocketService;
};

export const getWebSocketService = (): WebSocketService | null => {
  return webSocketService;
};

export const destroyWebSocket = () => {
  if (webSocketService) {
    webSocketService.destroy();
    webSocketService = null;
  }
};

export default WebSocketService;
