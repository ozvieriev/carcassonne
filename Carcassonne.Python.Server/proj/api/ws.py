from typing import Dict, Set, List
from fastapi import WebSocket
import logging
import random


logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage websocket connections per game room."""

    def __init__(self):
        self.id = random.randint(0, 10000)
        self.connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, gameId: str):
        await websocket.accept()
        newConnection = self.connections.setdefault(gameId, set())
        newConnection.add(websocket)

        targets = self.connections.get(gameId, [])

        await websocket.send_json({"type": "connected", "id": self.id, "gameId": gameId})

    def disconnect(self, websocket: WebSocket, gameId: str):
        gameConnection = self.connections.get(gameId)

        if not gameConnection:
            return

        gameConnection.discard(websocket)

        logger.info("WebSocket disconnected: game=%s, remaining=%d",
                    gameId, len(gameConnection))

        if len(gameConnection) == 0:
            del self.connections[gameId]

    async def send_personal_message(self, message: object, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: object, gameId: str):
        targets: List[WebSocket] = []

        if gameId is not None:
            targets = list(self.connections.get(gameId, []))
            
        logger.info("Broadcasting message to %d clients for game %s",
                    len(targets), gameId)

        for connection in targets:
            try:
                await connection.send_json(message)
            except Exception:
                logger.exception(
                    "Failed to send websocket message to a client in game %s", gameId)


manager = ConnectionManager()
