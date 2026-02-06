from fastapi import APIRouter, Depends
from ..repositories import *
from ..services import *

router = APIRouter()

def createGameService(repository=Depends(gameRepository)) -> gameService:
    return gameService(repository)

from . import gameRoute