from .tile import tile
from .point import point
from .player import player
from ..enums import *

class move:
    def __init__(self, player: player, tile: tile, location: point, rotation: tileRotation):
        self.playerId: str = player.id
        self.tile: "tile" = tile
        self.location: point = location
        self.rotation: tileRotation = rotation

    def to_dict(self) -> dict:
        return {
            "playerId": self.playerId,
            "tile": self.tile.to_dict(),
            "location": self.location.to_dict(),
            "rotation": self.rotation.value
        }
    
    @classmethod
    def from_dict(self, data: dict) -> "move":
        dataPlayerId = data.get("playerId", "")
        dataTile = data.get("tile", {})
        dataLocation = data.get("location", {})
        dataRotation = data.get("rotation", tileRotation.R0)

        p = player(dataPlayerId, "", "")
        t = tile.from_dict(dataTile)
        location = point.from_dict(dataLocation)
        rotation = tileRotation(dataRotation)

        return self(p, t, location, rotation)
