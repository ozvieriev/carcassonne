from typing import Iterable

class point():
    x: int
    y: int

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y
        }
    
    @classmethod
    def from_dict(self, data: dict) -> "point":
        x = data.get("x", 0)
        y = data.get("y", 0)
        
        return self(x, y)

    def neighbors(self) -> Iterable["point"]:
        yield point(self.x, self.y - 1)
        yield point(self.x + 1, self.y)
        yield point(self.x, self.y + 1)
        yield point(self.x - 1, self.y)
