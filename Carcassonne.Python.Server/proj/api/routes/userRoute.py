from datetime import datetime
from fastapi import Depends, HTTPException

from proj.api.models import *
from proj.api.services import *

from . import router, createUserService


@router.get("/user/{userId}")
def get_user(userId: int, service: userService = Depends(createUserService)):
    user = userModel()  # service.get(userId)

    print(f"/user/{userId}")

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return user
