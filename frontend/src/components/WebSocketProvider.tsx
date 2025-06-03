// Enhanced WebSocket provider with error handling and reconnection
import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  useRef,
} from "react";

export interface WebSocketMessage {
  type: string;
  payload?: unknown;
  timestamp?: string;
}

interface WebSocketContextType {
  socket: WebSocket | null;
  isConnected: boolean;
  isReconnecting: boolean;
  connectionStatus: "connecting" | "connected" | "disconnected" | "error";
  lastMessage: WebSocketMessage | null;
  sendMessage: (message: WebSocketMessage) => void;
  reconnect: () => void;
  disconnect: () => void;
}

const WebSocketContext = createContext<WebSocketContextType | null>(null);

// Export context for use in hook
export { WebSocketContext };

interface WebSocketProviderProps {
  children: React.ReactNode;
  url?: string;
  maxReconnectAttempts?: number;
  reconnectInterval?: number;
}

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({
  children,
  url = "ws://localhost:8000/ws",
  maxReconnectAttempts = 5,
  reconnectInterval = 3000,
}) => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [isReconnecting, setIsReconnecting] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<
    "connecting" | "connected" | "disconnected" | "error"
  >("disconnected");
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);

  const reconnectAttempts = useRef(0);
  const reconnectTimeoutRef = useRef<number | null>(null);
  const shouldReconnect = useRef(true);

  const connect = useCallback(() => {
    if (socket?.readyState === WebSocket.OPEN) {
      return; // Already connected
    }

    setConnectionStatus("connecting");

    try {
      const ws = new WebSocket(url);

      ws.onopen = () => {
        console.log("WebSocket connected");
        setSocket(ws);
        setIsConnected(true);
        setIsReconnecting(false);
        setConnectionStatus("connected");
        reconnectAttempts.current = 0;

        // Send initial connection message
        ws.send(
          JSON.stringify({
            type: "connection",
            timestamp: new Date().toISOString(),
          })
        );
      };

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          setLastMessage(message);
          console.log("WebSocket message received:", message);
        } catch (error) {
          console.error("Failed to parse WebSocket message:", error);
        }
      };

      ws.onclose = (event) => {
        console.log("WebSocket disconnected:", event.code, event.reason);
        setSocket(null);
        setIsConnected(false);
        setConnectionStatus("disconnected");

        // Attempt to reconnect if it wasn't a manual disconnect
        if (
          shouldReconnect.current &&
          reconnectAttempts.current < maxReconnectAttempts
        ) {
          setIsReconnecting(true);
          reconnectAttempts.current += 1;

          console.log(
            `Attempting to reconnect (${reconnectAttempts.current}/${maxReconnectAttempts})`
          );

          reconnectTimeoutRef.current = window.setTimeout(() => {
            connect();
          }, reconnectInterval);
        } else if (reconnectAttempts.current >= maxReconnectAttempts) {
          console.error("Max reconnection attempts reached");
          setConnectionStatus("error");
          setIsReconnecting(false);
        }
      };

      ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        setConnectionStatus("error");
      };
    } catch (error) {
      console.error("Failed to create WebSocket connection:", error);
      setConnectionStatus("error");
    }
  }, [url, maxReconnectAttempts, reconnectInterval, socket?.readyState]);

  const sendMessage = useCallback(
    (message: WebSocketMessage) => {
      if (socket?.readyState === WebSocket.OPEN) {
        const messageWithTimestamp = {
          ...message,
          timestamp: new Date().toISOString(),
        };
        socket.send(JSON.stringify(messageWithTimestamp));
      } else {
        console.warn("WebSocket is not connected. Message not sent:", message);
      }
    },
    [socket]
  );

  const reconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    reconnectAttempts.current = 0;
    shouldReconnect.current = true;
    connect();
  }, [connect]);

  const disconnect = useCallback(() => {
    shouldReconnect.current = false;
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    if (socket) {
      socket.close(1000, "Manual disconnect");
    }
    setIsReconnecting(false);
  }, [socket]);

  useEffect(() => {
    connect();

    return () => {
      shouldReconnect.current = false;
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (socket) {
        socket.close();
      }
    };
  }, [connect, socket]);

  const value: WebSocketContextType = {
    socket,
    isConnected,
    isReconnecting,
    connectionStatus,
    lastMessage,
    sendMessage,
    reconnect,
    disconnect,
  };

  return (
    <WebSocketContext.Provider value={value}>
      {children}
      {/* Connection status indicator */}
      {connectionStatus !== "connected" && (
        <div className="fixed top-4 right-4 z-50">
          <div
            className={`px-4 py-2 rounded-lg text-sm font-medium ${
              connectionStatus === "connecting" || isReconnecting
                ? "bg-yellow-100 text-yellow-800 border border-yellow-200"
                : connectionStatus === "error"
                ? "bg-red-100 text-red-800 border border-red-200"
                : "bg-gray-100 text-gray-800 border border-gray-200"
            }`}
          >
            {connectionStatus === "connecting" && "Connecting..."}
            {isReconnecting &&
              `Reconnecting... (${reconnectAttempts.current}/${maxReconnectAttempts})`}
            {connectionStatus === "error" && "Connection Error"}
            {connectionStatus === "disconnected" &&
              !isReconnecting &&
              "Disconnected"}

            {connectionStatus === "error" && (
              <button
                onClick={reconnect}
                className="ml-2 px-2 py-1 bg-red-600 text-white rounded text-xs hover:bg-red-700 transition-colors"
              >
                Retry
              </button>
            )}
          </div>
        </div>
      )}
    </WebSocketContext.Provider>
  );
};
