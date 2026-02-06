from fastapi import Depends, HTTPException

from proj.api.models import *
from proj.core.utils import *
from proj.core.factories import *
from proj.core.models import *
from . import createGameService, router
from ..services import *


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

    players = playerFactory.loadFromMap()
    tiles = tileFactory.loadFromMap()
    b = board(players, tiles)

    return gameApiModel.createInstance(game, b)


@router.put("/game/{gameId}/placeTile", )
def putGamePlaceTile(gameId: str, request: gamePlaceTileRequest, service: gameService = Depends(createGameService)):
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

    return gameApiModel.createInstance(game, b)
