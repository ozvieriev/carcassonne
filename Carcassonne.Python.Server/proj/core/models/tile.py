from ..enums import *
from .player import player
from dataclasses import dataclass
from typing import Optional

@dataclass
class tile:

    ANGLE_STEP = 90

    DIRECTIONS = [
        tileDirection.N,
        tileDirection.E,
        tileDirection.S,
        tileDirection.W,
    ]

    def __init__(self, edges: dict[tileDirection, tileEdge]):
        self.rotation = 0
        self.edges = edges
        self.playerId: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "rotation": self.rotation,
            #"edges": [self.edge(k) for k, v in self.edges.items()],
            #{f"{x},{y}": v.to_dict() for (x, y), v in self.tiles.items()}
            "playerId": self.playerId,
        }

    @classmethod
    def from_dict(self, data: dict):
        edges = {
            tileDirection[k]: tileEdge[v] for k, v in data["edges"].items()
        }

        return self(edges)

    def rotate(self):
        self.rotation = (self.rotation + self.ANGLE_STEP) % 360

        return self.rotation

    def edge(self, direction: tileDirection) -> tileEdge:
        steps = (self.rotation // self.ANGLE_STEP) % len(self.DIRECTIONS)

        if direction not in self.DIRECTIONS:
            return self.edges[direction]  # center or special

        idx = self.DIRECTIONS.index(direction)
        direction =  self.DIRECTIONS[(idx - steps) % len(self.DIRECTIONS)]

        return self.edges[direction]
    
    def edgeName(self, direction: tileDirection) -> tileEdge:
        
        edge = self.edge(direction)

        if(edge is not None):
            return edge.name[0]
        
        return None 

    def setPlayer(self, player: player) -> None:
        """Set the current player"""
        self.playerId = player.id

    def __repr__(self) -> str:
        return f"rotation={self.rotation}, edges={self.edges} , playerId={self.playerId}"
