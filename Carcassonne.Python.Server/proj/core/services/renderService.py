from ..models import *
from .htmlService import *


class renderService:
    def __init__(self, b: board, h: htmlService = htmlService()):
        self.board: board = b
        self.htmlService: htmlService = h

    def toHtml(self) -> str:
        html = ""

        for (x, y) in self.board.moves.keys():
            img = ""

            move = self.board.moves[(x, y)]

            if (move.tile.img):
                img = f"<img src='tiles/{move.tile.img}' />"

            x = (x * 75) + 500
            y = (y * 75) + 500
            html += f"<div class='tile r-{move.tile.rotation}' style='left: {x}px; top: {y}px;'>{img}</div>"

        data = {
            "body": f"<div class='board'>{html}</div>"
        }

        return self.htmlService.renderTemplate(data)

    def toJson(self) -> str:
        return json.dumps(self.board.to_dict())

    def getHtmlTemplate() -> str:
        with open("file.html", "r", encoding="utf-8") as f:
            return f.read()
