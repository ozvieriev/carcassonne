from ..models import *
import json, random


class tileFactory:
    @staticmethod
    def createTile(north: tileEdge, east: tileEdge, south: tileEdge, west: tileEdge, center: tileEdge = None) -> tile:
        edges = {
            tileDirection.N: north,
            tileDirection.E: east,
            tileDirection.S: south,
            tileDirection.W: west,
            tileDirection.C: center
        }

        return tile(edges)

    @staticmethod
    def loadFromMap(path: str = "proj/core/data/tiles.json"):

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        tiles = [tile.from_dict(item) for item in data]
        random.shuffle(tiles)
        
        return tiles
