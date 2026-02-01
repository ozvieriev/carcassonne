from typing import Tuple, Iterable


class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def toTuple(self) -> Tuple[int, int]:
        return (self.x, self.y)

    @classmethod
    def fromTuple(cls, t: Tuple[int, int]) -> "Point":
        return cls(t[0], t[1])

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def neighbors(self) -> Iterable["Point"]:
        yield Point(self.x, self.y - 1)
        yield Point(self.x + 1, self.y)
        yield Point(self.x, self.y + 1)
        yield Point(self.x - 1, self.y)
