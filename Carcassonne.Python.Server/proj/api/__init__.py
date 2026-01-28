from fastapi import APIRouter, Depends
from ..repositories.userRepository import userRepository
from ..services.userService import userService

router = APIRouter()

def createUserService(repository=Depends(userRepository)) -> userService:
    return userService(repository)

from . import userRoute