from ..models import *
import json
import random


class tileFactory:
    @staticmethod
    def createTile(north: tileEdge, east: tileEdge, south: tileEdge, west: tileEdge, center: tileEdge = None) -> tile:
        edges = {
            tileDirection.N: north,
            tileDirection.E: east,
            tileDirection.S: south,
            tileDirection.W: west
        }

        return tile("", edges)

    @staticmethod
    def loadFromMap():
        river = []
        base = []
        abbot = []
        inns = []

        def append(path: str, tiles: list):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for entry in data:
                tiles.append(tile.from_dict(entry))

        append("proj/core/data/tiles-river.json", river)
        append("proj/core/data/tiles-base.json", base)
        append("proj/core/data/tiles-abbot.json", abbot)
        random.shuffle(base)
        random.shuffle(abbot)
        random.shuffle(inns)

        tiles = river + base + abbot + inns

        return tiles
