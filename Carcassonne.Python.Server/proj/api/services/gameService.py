from ..repositories import *
from uuid import UUID


class gameService:
    def __init__(self, repository: gameRepository):
        self.repository = repository

    def get(self, id: int):
        return self.repository.get(id)

    def create(self, model: str):
        return self.repository.create(model)
