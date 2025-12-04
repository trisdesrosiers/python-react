import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Custom hook for WebSocket connection with auto-reconnect.
 * Listens for real-time database changes via PostgreSQL NOTIFY.
 */
export const useWebSocket = (options = {}) => {
    const { enabled = true } = options;
    
    // Use refs for callbacks to avoid reconnection on callback changes
    const onMessageRef = useRef(options.onMessage);
    const onConnectRef = useRef(options.onConnect);
    const onDisconnectRef = useRef(options.onDisconnect);
    
    // Update refs when callbacks change
    useEffect(() => {
        onMessageRef.current = options.onMessage;
        onConnectRef.current = options.onConnect;
        onDisconnectRef.current = options.onDisconnect;
    }, [options.onMessage, options.onConnect, options.onDisconnect]);

    const [isConnected, setIsConnected] = useState(false);
    const [lastMessage, setLastMessage] = useState(null);
    const wsRef = useRef(null);
    const reconnectTimeoutRef = useRef(null);
    const reconnectAttempts = useRef(0);
    const maxReconnectAttempts = 10;
    const baseReconnectDelay = 1000;
    const enabledRef = useRef(enabled);
    
    useEffect(() => {
        enabledRef.current = enabled;
    }, [enabled]);

    const getWebSocketUrl = useCallback(() => {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        return `${protocol}//${host}/ws/changes/`;
    }, []);

    const connect = useCallback(() => {
        if (!enabledRef.current) return;
        if (wsRef.current?.readyState === WebSocket.OPEN || 
            wsRef.current?.readyState === WebSocket.CONNECTING) {
            return; // Already connected or connecting
        }
        
        try {
            const url = getWebSocketUrl();
            wsRef.current = new WebSocket(url);

            wsRef.current.onopen = () => {
                setIsConnected(true);
                reconnectAttempts.current = 0;
                onConnectRef.current?.();
            };

            wsRef.current.onclose = (event) => {
                setIsConnected(false);
                onDisconnectRef.current?.();

                // Auto-reconnect with exponential backoff
                if (enabledRef.current && reconnectAttempts.current < maxReconnectAttempts) {
                    const delay = Math.min(
                        baseReconnectDelay * Math.pow(2, reconnectAttempts.current),
                        30000
                    );
                    reconnectAttempts.current++;
                    reconnectTimeoutRef.current = setTimeout(connect, delay);
                }
            };

            wsRef.current.onerror = () => {};

            wsRef.current.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    setLastMessage(data);
                    onMessageRef.current?.(data);
                } catch (e) {
                    // Silent fail on parse error
                }
            };
        } catch (error) {
            // Silent fail on connection error
        }
    }, [getWebSocketUrl]);

    const disconnect = useCallback(() => {
        if (reconnectTimeoutRef.current) {
            clearTimeout(reconnectTimeoutRef.current);
            reconnectTimeoutRef.current = null;
        }
        if (wsRef.current) {
            wsRef.current.close();
            wsRef.current = null;
        }
    }, []);

    const sendMessage = useCallback((message) => {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify(message));
        }
    }, []);

    // Connect on mount, disconnect on unmount
    useEffect(() => {
        if (enabled) {
            connect();
        }
        return () => {
            disconnect();
        };
    }, [enabled]); // Only depend on enabled, not connect/disconnect

    return {
        isConnected,
        lastMessage,
        sendMessage
    };
};

/**
 * Hook to subscribe to changes on specific tables.
 */
export const useTableChanges = (tables, onTableChange, enabled = true) => {
    const tableList = Array.isArray(tables) ? tables : [tables];
    const tableListRef = useRef(tableList);
    const onTableChangeRef = useRef(onTableChange);
    
    useEffect(() => {
        tableListRef.current = tableList;
        onTableChangeRef.current = onTableChange;
    }, [tableList, onTableChange]);

    const handleMessage = useCallback((message) => {
        if (message.type === 'db_change' && tableListRef.current.includes(message.table)) {
            onTableChangeRef.current?.({
                table: message.table,
                operation: message.operation,
                data: message.data
            });
        }
    }, []);

    return useWebSocket({
        onMessage: handleMessage,
        enabled
    });
};

export default useWebSocket;
