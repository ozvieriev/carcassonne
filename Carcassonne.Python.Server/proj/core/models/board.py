from typing import Dict, Tuple, Optional, List
from .tile import tile
from .player import player
from .move import move
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
            # "moves": {f"{x},{y}": v.to_dict() for (x, y), v in self.moves.items()},
            "players": [player.to_dict() for player in self.players]
        }

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

    def getCurrentPlayer(self) -> Optional[player]:
        if not self.players:
            return None

        if (not self.moves):
            return self.players[0]

        move = list(self.moves.values())[-1]

        index = indexOf(self.players,
                         lambda entity: entity.id == move.playerId)

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

        anyAvailable = self.getAnyAvailablePosition(tile)

        if (anyAvailable is None):
            self.skippedTiles.append(tile)
            return self.getNextTile()

        return tile

    def getMove(self, point: point) -> move | None:
        return self.moves.get((point.x, point.y))

    def getTile(self, x: int, y: int) -> tile | None:
        move = self.getMove(point(x, y))

        return move.tile if move else None

    def canPlaceTile(self, x: int, y: int, tile: tile, rotation: tileRotation = tileRotation.R0) -> bool:
        if (not self.moves):
            return True

        move = self.getMove(point(x, y))

        if move is not None:
            return False

        tileHasRiver = tile.anyEdge(tileEdge.RIVER)

        for direction, (nx, ny), opposite in self.getNeighbors(x, y):
            neighborMove = self.getMove(point(nx, ny))

            if neighborMove is None:
                continue

            edge = tile.edge(direction, rotation)
            neighborEdge = neighborMove.tile.edge(
                opposite, neighborMove.rotation)

            if tileHasRiver:
                neighborHasriver = neighborMove.tile.anyEdge(tileEdge.RIVER)

                if tileHasRiver or neighborHasriver:
                    if not (edge == tileEdge.RIVER and neighborEdge == tileEdge.RIVER):
                        return False

            if edge != neighborEdge:
                return False

        return True

    def placeTile(self, x: int, y: int, tile: tile, rotation: tileRotation = tileRotation.R0) -> bool:
        if not self.canPlaceTile(x, y, tile, rotation):
            return False

        player = self.getCurrentPlayer()

        tile.setPlayer(player)
        self.moves[(x, y)] = move(player, tile, point(x, y), rotation)

        return True

    def getAnyAvailablePosition(self, tile: tile) -> tuple[int, int] | None:
        if not self.moves:
            return (0, 0)

        rotations = list(tileRotation)

        for (x, y) in self.moves.keys():
            for _, (nx, ny), _ in self.getNeighbors(x, y):
                if (nx, ny) in self.moves:
                    continue

                for rotation in rotations:
                    if self.canPlaceTile(nx, ny, tile, rotation):
                        return (nx, ny)

        return None


    def getAvailablePositions(self, tile: tile) -> list[tuple[int, int]]:
        positions = set()

        if not self.moves:
            return [(0, 0)]

        rotations = list(tileRotation)

        for (x, y) in self.moves.keys():
            for _, (nx, ny), _ in self.getNeighbors(x, y):
                if (nx, ny) in self.moves:
                    continue

                for rotation in rotations:
                    if self.canPlaceTile(nx, ny, tile, rotation):
                        positions.add((nx, ny))
                        break

        return list(positions)

    def getNeighbors(self, x: int, y: int):
        yield (tileDirection.N, (x, y - 1), tileDirection.S)
        yield (tileDirection.E, (x + 1, y), tileDirection.W)
        yield (tileDirection.S, (x, y + 1), tileDirection.N)
        yield (tileDirection.W, (x - 1, y), tileDirection.E)