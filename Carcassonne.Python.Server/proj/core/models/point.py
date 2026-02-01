from typing import Tuple, Iterable

class point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def neighbors(self) -> Iterable["point"]:
        yield point(self.x, self.y - 1)
        yield point(self.x + 1, self.y)
        yield point(self.x, self.y + 1)
        yield point(self.x - 1, self.y)
