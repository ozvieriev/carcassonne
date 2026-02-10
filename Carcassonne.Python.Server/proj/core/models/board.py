from typing import Dict, Tuple, Optional, List
from .tile import tile
from .player import player
from .move import move
from .availableMove import availableMove
from .point import point
from ..utils import *
from ..enums import *
import logging
import json

# optional color support
try:
    from colorama import init as _colorama_init
    from colorama import Fore, Style, Back
    _colorama_init(autoreset=True)
    COLORAMA_AVAILABLE = True
except Exception:
    # colorama not available; fall back to no colors
    Fore = Style = Back = None
    COLORAMA_AVAILABLE = False


class board:
    def __init__(self, players: list[player], tiles: list[tile]):
        self.skippedTiles: list[tile] = []
        self.players: list[player] = players
        self.tiles: list[tile] = tiles
        self.moves: Dict[Tuple[int, int], move] = {}

    def to_dict(self) -> dict:
        return {
            "skippedTiles": [tile.to_dict() for tile in self.skippedTiles],
            "players": [player.to_dict() for player in self.players],
            "tiles": [tile.to_dict() for tile in self.tiles],
            "moves": [v.to_dict() for (x, y), v in self.moves.items()]
        }

    @classmethod
    def from_dict(self, data: dict) -> "board":
        dataSkippedTiles = data.get("skippedTiles", [])
        dataPlayers = data.get("players", [])
        dataTiles = data.get("tiles", [])
        dataMoves = data.get("moves", [])

        players = [player.from_dict(p) for p in dataPlayers]
        tiles = [tile.from_dict(t) for t in dataTiles]

        b = self(players, tiles)
        b.skippedTiles = [tile.from_dict(t) for t in dataSkippedTiles]
        b.moves = {}

        for mv in dataMoves:
            moveObj = move.from_dict(mv)
            x = moveObj.location.x
            y = moveObj.location.y
            b.moves[(x, y)] = moveObj

        return b

    def addPlayer(self, player: player) -> None:
        """Add a player to the game in turn order."""
        self.players.append(player)

    def addPlayers(self, players: list[player]) -> None:
        """Add multiple players to the game in the given order.

        This is a small convenience wrapper around repeated calls to
        addPlayer so callers can add a batch of players at once.
        """
        for p in players:
            self.addPlayer(p)

    def getPlayers(self) -> list[player]:
        return list(self.players)

    def getCurrentPlayer(self) -> player | None:
        if not self.players:
            return None

        if (not self.moves):
            return self.players[0]

        move = list(self.moves.values())[-1]

        index = indexOf(self.players,
                        lambda entity: entity.id == move.playerId)

        return nextItem(self.players, index)

    def getNextPlayer(self) -> player | None:
        if not self.players:
            return None

        current = self.getCurrentPlayer()

        if current is None:
            return nextItem(self.players, 0)

        index = indexOf(self.players, lambda entity: entity.id == current.id)

        return nextItem(self.players, index)

    def getNextTile(self) -> Optional[tile]:
        if not self.tiles:
            return None

        index = len(self.moves) + len(self.skippedTiles)

        if (index >= len(self.tiles)):
            return None

        tile = self.tiles[index]

        if (tile is None):
            return None

        anyAvailable = self.getAnyAvailableMove(tile)

        if (anyAvailable is None):
            self.skippedTiles.append(tile)
            return self.getNextTile()

        return tile

    def getMove(self, point: point) -> move | None:
        return self.moves.get((point.x, point.y))

    def getTile(self, x: int, y: int) -> tile | None:
        move = self.getMove(point(x, y))

        return move.tile if move else None

    def canPlaceTile(self, location: point, tile: tile, rotation: tileRotation = tileRotation.R0) -> bool:
        """Return True if `tile` (with rotation) can be placed at `location`.

        `location` is a `point` instance. This replaces the previous x,y signature.
        """
        if (not self.moves):
            return True

        move = self.getMove(location)

        if move is not None:
            return False

        tileHasRiver = tile.anyEdge(tileEdge.RIVER)

        for direction, (nx, ny), opposite in self.getNeighbors(location.x, location.y):
            neighborMove = self.getMove(point(nx, ny))

            if neighborMove is None:
                continue

            edge = tile.getEdge(direction, rotation)
            neighborEdge = neighborMove.tile.getEdge(
                opposite, neighborMove.rotation)

            if tileHasRiver:
                neighborHasRiver = neighborMove.tile.anyEdge(tileEdge.RIVER)

                if neighborHasRiver:
                    if not (edge == tileEdge.RIVER and neighborEdge == tileEdge.RIVER):
                        return False

            if edge != neighborEdge:
                return False

        return True

    def placeTile(self, location: point, tile: tile, rotation: tileRotation = tileRotation.R0) -> bool:
        """Place `tile` at `location` (a `point`) with the given rotation.

        Returns True if placement succeeded.
        """
        if not self.canPlaceTile(location, tile, rotation):
            return False

        player = self.getCurrentPlayer()

        self.moves[(location.x, location.y)] = move(player, tile, location, rotation)

        return True

    def getAnyAvailableMove(self, tile: tile) -> Optional[availableMove]:
        """Return a single availableMove (location + valid rotations) for the given tile, or None."""
        
        rotations = tileRotation.getAllRotations()
        
        if not self.moves:
            return availableMove(point(0, 0), tile, rotations)

        for (x, y) in self.moves.keys():
            for _, (nx, ny), _ in self.getNeighbors(x, y):
                if (nx, ny) in self.moves:
                    continue

                location = point(nx, ny)
                validRotations: List[tileRotation] = []

                for rotation in rotations:
                    if self.canPlaceTile(location, tile, rotation):
                        validRotations.append(rotation)

                if validRotations:
                    return availableMove(location, tile, validRotations)

        return None

    def getAvailableMoves(self, tile: tile) -> list[availableMove]:
        """Return a list of availableMove objects (location + rotations) for the given tile."""
        
        rotations = tileRotation.getAllRotations()
        availableMoves: List[availableMove] = []

        if not self.moves:
            availableMoves.append(availableMove(point(0, 0), tile, rotations))
            return availableMoves

        for (x, y) in self.moves.keys():
            for _, (nx, ny), _ in self.getNeighbors(x, y):
                if (nx, ny) in self.moves:
                    continue

                location = point(nx, ny)
                validRotations: List[tileRotation] = []

                for rotation in rotations:
                    if self.canPlaceTile(location, tile, rotation):
                        validRotations.append(rotation)

                if validRotations:
                    availableMoves.append(availableMove(location, tile, validRotations))

        return availableMoves

    def getNeighbors(self, x: int, y: int):
        yield (tileDirection.N, (x, y - 1), tileDirection.S)
        yield (tileDirection.E, (x + 1, y), tileDirection.W)
        yield (tileDirection.S, (x, y + 1), tileDirection.N)
        yield (tileDirection.W, (x - 1, y), tileDirection.E)
