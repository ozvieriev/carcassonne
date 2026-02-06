from typing import Dict, Set, List
from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage websocket connections per game room."""

    def __init__(self):
        self.connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, gameId: str):
        await websocket.accept()

        connection = self.connections.setdefault(gameId, set())
        connection.add(websocket)

        await websocket.send_json({"type": "connect", "gameId": gameId})

    def disconnect(self, websocket: WebSocket, gameId: str):
        connection = self.connections.get(gameId)

        if not connection:
            return

        connection.discard(websocket)

        logger.info(
            f"WebSocket disconnected: game={gameId}, remaining={len(connection)}")

        if len(connection) == 0:
            del self.connections[gameId]

    async def personal(self, message: object, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: object, gameId: str):
        webSockets: List[WebSocket] = []

        if gameId is not None:
            webSockets = list(self.connections.get(gameId, []))

        logger.info("Broadcasting message to %d clients for game %s",
                    len(webSockets), gameId)

        for websocket in webSockets:
            try:
                await websocket.send_json(message)
            except Exception:
                logger.exception(
                    f"Failed to send websocket message to a client in game {gameId}")


manager = ConnectionManager()
