from .tile import tile
from .point import point
from .player import player
from ..enums import *

class move:
    def __init__(self, player: player, tile: tile, location: point, rotation: tileRotation):
        self.playerId: int = player.id
        self.tile = tile
        self.location: point = location
        self.rotation: tileRotation = rotation

    def to_dict(self) -> dict:
        return {
            "playerId": self.playerId,
            "tile": self.tile.to_dict(),
            "location": self.location.to_dict(),
            "rotation": self.rotation.value
        }