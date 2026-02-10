from ..enums import *
from typing import Optional


class tile:

    ANGLE_STEP = 90

    EDGES = [
        tileDirection.N,
        tileDirection.E,
        tileDirection.S,
        tileDirection.W,
    ]

    CHAR_EDGE_PAIRS = {
        'C': tileEdge.CITY,
        'R': tileEdge.ROAD,
        'F': tileEdge.FIELD,
        'M': tileEdge.MONASTERY,
        'r': tileEdge.RIVER,
    }

    EDGE_TO_CHAR = {edge: char for char, edge in CHAR_EDGE_PAIRS.items()}

    def __init__(self, img: str, edges: str):
        self.img: str = img
        self.edges: str = edges

    def to_dict(self) -> dict:

        return {
            "img": self.img,
            "edges": self.edges
        }

    @classmethod
    def from_dict(self, data: dict):
        
        img = data.get("img", "")
        edges = data.get("edges", "")

        return self(img, edges)

    def getEdge(self, direction: tileDirection, rotation: tileRotation = tileRotation.R0) -> tileEdge:
        steps = (rotation.value // self.ANGLE_STEP) % len(self.EDGES)

        if direction not in self.EDGES:
            return self.edges[direction]  # center or special

        idx = self.EDGES.index(direction)
        direction = self.EDGES[(idx - steps) % len(self.EDGES)]
        
        idx = self.EDGES.index(direction)

        edge =  self.edges[idx]

        return self.CHAR_EDGE_PAIRS.get(edge)

    def anyEdge(self, edge: tileEdge) -> bool:

        char = self.EDGE_TO_CHAR[edge]
        anyEdge = char in self.edges

        return anyEdge

    def __repr__(self) -> str:
        return f"edges={self.edges}"
