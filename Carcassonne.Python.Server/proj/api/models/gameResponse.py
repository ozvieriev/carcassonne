from .gameModel import gameModel
from proj.core.utils import *
from proj.core.models import *


class gameApiModel:
    id: str
    nextTile: tile | None
    nextPlayerId: int | str
    availablePositions: list[point]
    # totalMoves: int

    @staticmethod
    def createInstance(game: gameModel, board: board) -> "gameApiModel":

        nextTile = board.getNextTile()
        nextPlayer = board.getNextPlayer()

        model = gameApiModel()

        model.id = encodeBase62(game.id)
        model.nextTile = nextTile.to_dict() if nextTile else None
        model.nextPlayerId = nextPlayer.id if nextPlayer else None
        model.availablePositions = board.getAvailablePositions(
            nextTile) if nextTile else None
        # model.totalMoves = len(board.moves)

        return model


# class gameResponse:
#     def __init__(self, game: gameModel, board: board):
#         self.game = game
#         self.board = board

#     def to_dict(self) -> dict:

#         nextTile = self.board.getNextTile()
#         nextPlayer = self.board.getNextPlayer()
#         availablePositions = self.board.getAvailablePositions(nextTile)

#         return {
#             "id": encodeBase62(self.game.id),
#             "nextTile": nextTile.to_dict() if nextTile else None,
#             "nextPlayerId": nextPlayer.id if nextPlayer else None,
#             "availablePositions": availablePositions
#         }
