from .gameModel import *
from proj.core.utils import *
from proj.core.models import *


class gameResponse:
    def __init__(self, game: gameModel, board: board):
        self.game = game
        self.board = board

    def to_dict(self) -> dict:
        
        nextTile = self.board.getNextTile()
        nextPlayer = self.board.getNextPlayer()

        return {
            "id": encodeBase62(self.game.id),
            "board": self.board.to_dict(),
            "nextTile": nextTile.to_dict() if nextTile else None,
            "nextPlayerId": nextPlayer.id if nextPlayer else None,
        }
