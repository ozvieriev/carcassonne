from ..repositories import *
from proj.core.utils import *
from proj.api.models import *

class gameService:
    def __init__(self, repository: gameRepository):
        self.repository = repository

    def get(self, id: int):
        return self.repository.get(id)
    
    def getGame(self, id: str):
        return self.get(decodeBase62(id))

    def create(self, model: str):
        return self.repository.create(model)
    
    def update(self, game: gameModel):
        return self.repository.updateModel(game)
