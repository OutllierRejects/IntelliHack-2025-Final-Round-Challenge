import React, { useEffect, useRef } from 'react';
import { useAuthStore } from '../../store';
import { useRequestStore, useTaskStore, useNotificationStore } from '../../store';
import { toast } from 'react-hot-toast';

interface WebSocketMessage {
  type: 'request_created' | 'request_updated' | 'task_assigned' | 'task_updated' | 'notification' | 'agent_status';
  payload: any;
}

export const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const wsRef = useRef<WebSocket | null>(null);
  const { user, isAuthenticated } = useAuthStore();
  const { addRequest, updateRequest } = useRequestStore();
  const { addTask, updateTask } = useTaskStore();
  const { addNotification } = useNotificationStore();

  useEffect(() => {
    if (!isAuthenticated || !user) {
      return;
    }

    // Connect to WebSocket
    const wsUrl = `${import.meta.env.VITE_WS_URL || 'ws://localhost:8000'}/ws`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket connected');
      // Send authentication
      ws.send(JSON.stringify({
        type: 'auth',
        token: localStorage.getItem('auth_token'),
      }));
    };

    ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        handleWebSocketMessage(message);
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      // Attempt to reconnect after 5 seconds
      setTimeout(() => {
        if (isAuthenticated && user) {
          // Reconnect logic would go here
        }
      }, 5000);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [isAuthenticated, user]);

  const handleWebSocketMessage = (message: WebSocketMessage) => {
    switch (message.type) {
      case 'request_created':
        addRequest(message.payload);
        toast.success(`New emergency request: ${message.payload.title}`);
        break;

      case 'request_updated':
        updateRequest(message.payload.id, message.payload);
        // Only show toast for important status changes
        if (message.payload.status === 'assigned' || message.payload.status === 'completed') {
          toast.info(`Request ${message.payload.status}: ${message.payload.title}`);
        }
        break;

      case 'task_assigned':
        addTask(message.payload);
        if (message.payload.assigned_to === user?.id) {
          toast.success(`New task assigned: ${message.payload.title}`);
        }
        break;

      case 'task_updated':
        updateTask(message.payload.id, message.payload);
        if (message.payload.assigned_to === user?.id) {
          toast.info(`Task updated: ${message.payload.title}`);
        }
        break;

      case 'notification':
        addNotification(message.payload);
        // Show toast for high priority notifications
        if (message.payload.priority === 'high' || message.payload.priority === 'critical') {
          toast.error(message.payload.message);
        } else {
          toast.info(message.payload.message);
        }
        break;

      case 'agent_status':
        // Handle AGNO agent status updates
        console.log('Agent status update:', message.payload);
        break;

      default:
        console.log('Unknown WebSocket message type:', message.type);
    }
  };

  return <>{children}</>;
};

// Hook for sending WebSocket messages
export const useWebSocket = () => {
  const wsRef = useRef<WebSocket | null>(null);

  const sendMessage = (message: any) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  };

  return { sendMessage };
};
