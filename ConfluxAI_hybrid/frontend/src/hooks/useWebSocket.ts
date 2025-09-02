import { useState, useEffect, useCallback } from 'react';
import { getWebSocketService, WebSocketEvents } from '../services/websocket';

interface WebSocketState {
  isConnected: boolean;
  progress: number;
  lastMessage: any;
}

export const useWebSocket = () => {
  const [state, setState] = useState<WebSocketState>({
    isConnected: false,
    progress: 0,
    lastMessage: null,
  });

  const subscribe = useCallback(<K extends keyof WebSocketEvents>(
    event: K,
    callback: WebSocketEvents[K]
  ) => {
    const wsService = getWebSocketService();
    if (wsService) {
      return wsService.on(event, callback);
    }
    return () => {};
  }, []);

  const unsubscribe = useCallback((event: string) => {
    const wsService = getWebSocketService();
    if (wsService) {
      wsService.unsubscribe(event);
    }
  }, []);

  useEffect(() => {
    const wsService = getWebSocketService();
    if (wsService) {
      const unsubConnection = wsService.on('connection', (data: any) => {
        setState(prev => ({
          ...prev,
          isConnected: data.status === 'connected'
        }));
      });

      return () => {
        unsubConnection();
      };
    }
  }, []);

  return {
    isConnected: state.isConnected,
    progress: state.progress,
    subscribe,
    unsubscribe,
  };
};