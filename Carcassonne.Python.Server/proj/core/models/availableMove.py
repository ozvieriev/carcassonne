from typing import List
from .tile import tile
from .point import point
from ..enums import *


class availableMove:
    def __init__(self, location: point, tile: tile, rotations: set[tileRotation]):
        self.location: point = location
        self.tile: "tile" = tile
        self.rotations: set[tileRotation] = rotations

    def to_dict(self) -> dict:
        return {
            "location": self.location.to_dict(),
            "tile": self.tile.to_dict(),
            "rotations": [r.value for r in self.rotations]
        }

    @classmethod
    def from_dict(self, data: dict) -> "availableMove":
        dataLocation = data.get("location", {})
        dataTile = data.get("tile", {})
        dataRotations = data.get("rotations", [])

        location = point.from_dict(dataLocation)
        t = tile.from_dict(dataTile)
        rotations = {tileRotation(r) for r in dataRotations}

        return self(location, t, rotations)

    def __repr__(self) -> str:
        return f"availableMove(location={self.location}, tile={self.tile}, rotations={self.rotations})"
