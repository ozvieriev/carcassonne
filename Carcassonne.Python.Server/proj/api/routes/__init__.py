from fastapi import APIRouter, Depends
from ..repositories import *
from ..services import *

router = APIRouter()

def createUserService(repository=Depends(userRepository)) -> userService:
    return userService(repository)


def createGameService(repository=Depends(gameRepository)) -> gameService:
    return gameService(repository)

from . import gameRoute
from . import userRoute