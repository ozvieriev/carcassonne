from datetime import datetime
from fastapi import Depends, HTTPException

from proj.api.models import *
from proj.core.utils import *
from proj.core.factories import *
from proj.core.models import *

from . import createGameService, router, createGameService
from ..services import *


@router.put("/game/")
def putGame(service: gameService = Depends(createGameService)):
    players = playerFactory.loadFromMap()
    tiles = tileFactory.loadFromMap()
    b = board(players, tiles)

    model = str(b.to_dict())
    game = service.create(model)

    return gameResponse(game, b).to_dict()

@router.get("/game/{gameId}")
def getGame(gameId: str, service: gameService = Depends(createGameService)):
    game = service.get(decodeBase62(gameId))

    if not game:
        raise HTTPException(status_code=404, detail="not found")

    return gameResponse(game, b).to_dict()

