from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import List
import json
import logging
from datetime import datetime

from ...services.auth_service import get_current_user_from_websocket
from ...services.notification_service import NotificationService
from ...services.redis_client import get_redis_client

logger = logging.getLogger(__name__)

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str = None):
        await websocket.accept()
        self.active_connections.append(websocket)

        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = []
            self.user_connections[user_id].append(websocket)

        logger.info(
            f"WebSocket connected. Total connections: {len(self.active_connections)}"
        )

    def disconnect(self, websocket: WebSocket, user_id: str = None):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

        if user_id and user_id in self.user_connections:
            if websocket in self.user_connections[user_id]:
                self.user_connections[user_id].remove(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

        logger.info(
            f"WebSocket disconnected. Total connections: {len(self.active_connections)}"
        )

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def send_to_user(self, message: str, user_id: str):
        if user_id in self.user_connections:
            connections = self.user_connections[user_id].copy()
            for websocket in connections:
                try:
                    await websocket.send_text(message)
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id}: {e}")
                    self.disconnect(websocket, user_id)

    async def broadcast(self, message: str):
        connections = self.active_connections.copy()
        for connection in connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                if connection in self.active_connections:
                    self.active_connections.remove(connection)


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """General WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Handle different message types
            if message_data.get("type") == "ping":
                await manager.send_personal_message(
                    json.dumps(
                        {"type": "pong", "timestamp": datetime.utcnow().isoformat()}
                    ),
                    websocket,
                )
            elif message_data.get("type") == "connection":
                await manager.send_personal_message(
                    json.dumps(
                        {
                            "type": "connection_ack",
                            "message": "Connected to disaster response system",
                            "timestamp": datetime.utcnow().isoformat(),
                        }
                    ),
                    websocket,
                )
            else:
                # Echo back unhandled messages
                await manager.send_personal_message(
                    json.dumps(
                        {
                            "type": "echo",
                            "original": message_data,
                            "timestamp": datetime.utcnow().isoformat(),
                        }
                    ),
                    websocket,
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@router.websocket("/ws/{user_id}")
async def websocket_user_endpoint(websocket: WebSocket, user_id: str):
    """User-specific WebSocket endpoint for personalized updates"""
    await manager.connect(websocket, user_id)
    try:
        # Send welcome message
        await manager.send_personal_message(
            json.dumps(
                {
                    "type": "welcome",
                    "message": f"Connected as user {user_id}",
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ),
            websocket,
        )

        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Handle different message types
            if message_data.get("type") == "ping":
                await manager.send_personal_message(
                    json.dumps(
                        {
                            "type": "pong",
                            "user_id": user_id,
                            "timestamp": datetime.utcnow().isoformat(),
                        }
                    ),
                    websocket,
                )
            elif message_data.get("type") == "subscribe":
                # Handle subscription to specific updates
                topic = message_data.get("topic")
                await manager.send_personal_message(
                    json.dumps(
                        {
                            "type": "subscription_ack",
                            "topic": topic,
                            "user_id": user_id,
                            "timestamp": datetime.utcnow().isoformat(),
                        }
                    ),
                    websocket,
                )
            else:
                # Echo back with user context
                await manager.send_personal_message(
                    json.dumps(
                        {
                            "type": "echo",
                            "user_id": user_id,
                            "original": message_data,
                            "timestamp": datetime.utcnow().isoformat(),
                        }
                    ),
                    websocket,
                )
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        manager.disconnect(websocket, user_id)


# Utility functions for sending notifications through WebSocket
async def send_incident_update(incident_id: str, update_data: dict):
    """Send incident update to all connected clients"""
    message = json.dumps(
        {
            "type": "incident_update",
            "incident_id": incident_id,
            "data": update_data,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
    await manager.broadcast(message)


async def send_user_notification(user_id: str, notification_data: dict):
    """Send notification to specific user"""
    message = json.dumps(
        {
            "type": "notification",
            "data": notification_data,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
    await manager.send_to_user(message, user_id)


async def send_system_alert(alert_data: dict):
    """Send system-wide alert to all connected clients"""
    message = json.dumps(
        {
            "type": "system_alert",
            "data": alert_data,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
    await manager.broadcast(message)


# Export manager for use in other modules
websocket_manager = manager
