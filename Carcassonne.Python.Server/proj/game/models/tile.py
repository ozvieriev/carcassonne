from ..enums import *

class tile:

    DIRECTIONS = (
        tileDirection.N,
        tileDirection.E,
        tileDirection.S,
        tileDirection.W,
    )

    def __init__(self, edges: dict[tileDirection, tileEdge]):
        self.x = 0
        self.y = 0
        self.rotation = 0
        self.edges = edges

    def rotate(self):
        self.rotation = (self.rotation + 90) % 360

        return self.rotation

    def edge(self, direction: tileDirection) -> tileEdge:
        steps = (self.rotation // 90) % len(self.DIRECTIONS)

        if direction not in self.DIRECTIONS:
            return self.edges[direction]  # center or special

        idx = self.DIRECTIONS.index(direction)
        direction =  self.DIRECTIONS[(idx - steps) % 4]

        return self.edges[direction]

    def __repr__(self) -> str:
        return f"Tile(rotation={self.rotation}, edges={self.edges})"
