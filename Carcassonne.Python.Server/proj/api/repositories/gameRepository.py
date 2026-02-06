from datetime import datetime, timezone
from fastapi import Depends

from ..db import getDb
from ..models import *


class gameRepository:
    def __init__(self, db=Depends(getDb)):
        self.db = db

    def get(self, id: int) -> gameModel | None:
        return self.db.query(gameModel).filter(gameModel.id == id).first()
    
    def create(self, model: str) -> gameModel:

        game = gameModel()
        game.model = model
        game.createDateUtc = datetime.now(timezone.utc)

        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)

        return game

    def updateModel(self, game: gameModel) -> gameModel | None:
        if game is None:
            return None

        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)

        return game