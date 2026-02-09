from urllib import response
from fastapi import Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
import json

from proj.api.models import *
from proj.core.utils import *
from proj.core.factories import *
from proj.core.models import *
from . import createGameService, router
from ..services import *
from proj.api.ws import manager


@router.put("/game/")
def putGame(service: gameService = Depends(createGameService)):
    players = playerFactory.loadFromMap()
    tiles = tileFactory.loadFromMap()
    b = board(players, tiles)

    t = b.getNextTile()
    b.placeTile(0, 0, t)

    model = json.dumps(b.to_dict())
    game = service.create(model)

    return gameApiModel.createInstance(game, b)


@router.get("/game/{gameId}")
def getGame(gameId: str, service: gameService = Depends(createGameService)):
    game = service.getGame(gameId)

    if not game:
        raise HTTPException(status_code=404, detail="not found")

    b = board.from_dict(json.loads(game.model))

    return gameApiModel.createInstance(game, b)


@router.put("/game/{gameId}/placeTile", )
async def putGamePlaceTile(gameId: str, request: gamePlaceTileRequest, service: gameService = Depends(createGameService)):
    game = service.getGame(gameId)

    if not game:
        raise HTTPException(status_code=404, detail="not found")

    b = board.from_dict(json.loads(game.model))
    nextTile = b.getNextTile()

    if nextTile is None:
        raise HTTPException(status_code=400, detail="no next tile available")

    if (b.placeTile(request.location.x, request.location.y, nextTile, tileRotation(request.rotation)) is False):
        raise HTTPException(status_code=400, detail="invalid tile placement")

    game.model = json.dumps(b.to_dict())
    game = service.update(game)

    response = gameApiModel.createInstance(game, b)

    message = jsonable_encoder(response)
    message["type"] = "placeTile"

    await manager.broadcast(message, gameId)

    return response


@router.websocket("/ws/{gameId}")
async def websocket_endpoint(*, websocket: WebSocket, gameId: str, service: gameService = Depends(createGameService)):
    """Simple websocket endpoint to subscribe to game updates.

    Clients should connect to `/ws/{gameId}`. The server will accept the connection
    and send JSON messages when the board changes (for example, when a tile is placed).
    The endpoint echoes received text as an acknowledgement; it's tolerant to disconnects.
    """

    game = service.getGame(gameId)

    if not game:
        raise HTTPException(status_code=404, detail="not found")

    await manager.connect(websocket, gameId)

    try:
        while True:
            data = await websocket.receive_text()

            await manager.send_personal_message({"type": "ack", "data": data}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, gameId)
