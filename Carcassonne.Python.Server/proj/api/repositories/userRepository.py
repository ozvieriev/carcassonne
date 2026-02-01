from fastapi import Depends

from ..db import getDb
from ..models import userModel


class userRepository:
    def __init__(self, db=Depends(getDb)):
        self.db = db

    def get(self, id: int) -> userModel | None:
        return self.db.query(userModel).filter(userModel.pkID == id).first()
        #return userModel(id=id, email="example2@example.com")
