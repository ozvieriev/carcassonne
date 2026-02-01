from datetime import datetime
from fastapi import Depends, HTTPException

from . import router, createUserService
from ..services.userService import userService

@router.get("/user/{userId}")
def get_user(userId: int, service: userService = Depends(createUserService)):
    user = service.get(userId)

    print(f"/user/{userId}")

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return user

