from ..models import *
from .htmlService import *


class renderService:
    def __init__(self, b: board, h: htmlService = htmlService()):
        self.board: board = b
        self.htmlService: htmlService = h

    def toHtml(self, nextTile: tile = None) -> str:
        html = self.htmlService.renderTemplate({
            "offsetX": 30,
            "offsetY": 30,
            "moves": self.board.moves.values()
        }, templateName="board")

        return self.htmlService.renderTemplate({"body": html}, templateName="template")

    def toJson(self) -> str:
        return json.dumps(self.board.to_dict())

    def getHtmlTemplate() -> str:
        with open("file.html", "r", encoding="utf-8") as f:
            return f.read()
