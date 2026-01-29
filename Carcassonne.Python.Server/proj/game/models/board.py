from typing import Dict, Tuple, Optional
from .tile import tile
from ..enums import *


class board:
    def __init__(self):
        self.tiles: Dict[Tuple[int, int], tile] = {}

    def getTile(self, x: int, y: int) -> Optional[tile]:
        return self.tiles.get((x, y))

    def canPlaceTile(self, x: int, y: int, tile: tile) -> bool:

        if (len(self.tiles)) == 0:
            return True

        if (x, y) in self.tiles:
            return False

        for direction, (nx, ny), opposite in self.neighbors(x, y):
            neighbor = self.getTile(nx, ny)

            if neighbor is None:
                continue

            edge = tile.edge(direction)
            neighborEdge = neighbor.edge(opposite)

            if edge != neighborEdge:
                return False

        return True

    def placeTile(self, x: int, y: int, tile: tile) -> bool:

        if not self.canPlaceTile(x, y, tile):
            return False

        self.addTile(x, y, tile)
        return True

    def addTile(self, x: int, y: int, tile: tile):
        self.tiles[(x, y)] = tile

    def removeTile(self, x: int, y: int):
        self.tiles.pop((x, y))

    def neighbors(self, x: int, y: int):
        yield (tileDirection.N, (x, y - 1), tileDirection.S)
        yield (tileDirection.E, (x + 1, y), tileDirection.W)
        yield (tileDirection.S, (x, y + 1), tileDirection.N)
        yield (tileDirection.W, (x - 1, y), tileDirection.E)
