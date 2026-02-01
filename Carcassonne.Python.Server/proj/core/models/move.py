from .tile import tile
from .point import point
from .player import player

class move:
    def __init__(self, player: player, tile: tile, location: point, rotation: int):
        self.playerId: int = player.id
        self.tile = tile
        self.location: point = location
        self.rotation: int = rotation