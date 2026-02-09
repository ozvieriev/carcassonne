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

    CHARS = {
        'C': tileEdge.CITY,
        'R': tileEdge.ROAD,
        'F': tileEdge.FIELD,
        'M': tileEdge.MONASTERY,
        'r': tileEdge.RIVER,
    }

    def __init__(self, img: str, edges: dict[tileDirection, tileEdge]):
        self.img: str = img
        self.edges = edges

    def to_dict(self) -> dict:

        return {
            "img": self.img,
            "edges": {d.name: e.name for d, e in self.edges.items()}
        }

    @classmethod
    def from_dict(self, data: dict):
        raw = data["edges"]

        if isinstance(raw, str):
            
            if len(raw) != 4:
                raise ValueError("edges string must be 4 characters in NESW order")

            edges = {
                tileDirection.N: self.CHARS[raw[0]],
                tileDirection.E: self.CHARS[raw[1]],
                tileDirection.S: self.CHARS[raw[2]],
                tileDirection.W: self.CHARS[raw[3]],
            }
        else:
            edges = {tileDirection[k]: tileEdge[v] for k, v in raw.items()}

        return self(data.get("img", ""), edges)

    def edge(self, direction: tileDirection, rotation: tileRotation = tileRotation.R0) -> tileEdge:
        steps = (rotation.value // self.ANGLE_STEP) % len(self.EDGES)

        if direction not in self.EDGES:
            return self.edges[direction]  # center or special

        idx = self.EDGES.index(direction)
        direction = self.EDGES[(idx - steps) % len(self.EDGES)]

        return self.edges[direction]
    
    def anyEdge(self, edge: tileEdge) -> bool:
        return any(self.edges[d] == edge for d in self.EDGES)

    def edgeName(self, direction: tileDirection) -> tileEdge:
        
        edge = self.edge(direction)

        if(edge is not None):
            return edge.name[0]
        
        return None

    def __repr__(self) -> str:
        return f"edges={self.edges}"
