from ..models import *
from .htmlService import *


class renderService:
    def __init__(self, b: board, h: htmlService = htmlService()):
        self.board: board = b
        self.htmlService: htmlService = h

    def toHtml(self, nextTile: tile = None) -> str:
        size = 75
        offset = 600
        
        html = ""
        htmlNextTile = ""

        for (x, y) in self.board.moves.keys():
            move = self.board.moves[(x, y)]
            img = f"<img src='tiles/{move.tile.img}' />"

            x = (x * size) + offset
            y = (y * size) + offset
            html += f"<div class='tile r-{move.rotation.value}' style='left: {x}px; top: {y}px;'>{img}</div>"

        if(nextTile is not None):
            img = f"<img src='tiles/{nextTile.img}' />"
            htmlNextTile += f"<div class='tile r-0'>{img}</div>"

            for (x, y) in self.board.getAvailablePositions(nextTile):

                x = (x * size) + offset
                y = (y * size) + offset
                html += f"<div class='tile r-0' style='left: {x}px; top: {y}px;'></div>"
            
        data = {
            "body": f"<div class='board'>{htmlNextTile}</div><div class='board'>{html}</div>"
        }

        return self.htmlService.renderTemplate(data)

    def toJson(self) -> str:
        return json.dumps(self.board.to_dict())

    def getHtmlTemplate() -> str:
        with open("file.html", "r", encoding="utf-8") as f:
            return f.read()
