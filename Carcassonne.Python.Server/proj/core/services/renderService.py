from ..models import *
from .htmlService import *
from math import *

class renderService:
    def __init__(self, b: board, h: htmlService = htmlService()):
        self.board: board = b
        self.htmlService: htmlService = h

    def toHtml(self, nextTile: tile = None) -> str:

        xs = [x for (x, y) in self.board.moves.keys()]
        ys = [y for (x, y) in self.board.moves.keys()]

        minX = min(xs, default=0)
        maxX = max(xs, default=0)

        minY = min(ys, default=0)
        maxY = max(ys, default=0)

        cols = maxX - minX + 3
        rows = maxY - minY + 3

        html = self.htmlService.renderTemplate({
            "offsetX": 2 - minX,
            "offsetY": 2 - minY,
            "cols": cols,
            "rows": rows,
            "moves": self.board.moves.values(),
            "players": self.board.getPlayers()
        }, templateName="board")

        return html

    def toJson(self) -> str:
        return json.dumps(self.board.to_dict())
