from .gameModel import gameModel
from proj.core.utils import *
from proj.core.models import *

class gameApiModel():
    id: str
    nextTile: tile | None
    nextPlayerId: str
    availablePositions: list[point]
    moves: list[move]
    players: list[player]

    @staticmethod
    def createInstance(game: gameModel, board: board) -> "gameApiModel":
        
        nextTile = board.getNextTile()
        nextPlayer = board.getNextPlayer()
        
        model = gameApiModel()
        
        model.id = encodeBase62(game.id)
        model.nextTile = nextTile.to_dict() if nextTile else None
        model.nextPlayerId = nextPlayer.id if nextPlayer else None
        model.availablePositions = board.getAvailablePositions(nextTile) if nextTile else None
        model.moves = [v for (x, y), v in board.moves.items()]
        model.players = [p.to_dict() for p in board.getPlayers()]

        return model