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
        self.players: list[player] = players
        self.tiles: list[tile] = tiles
        self.dictMoves: Dict[Tuple[int, int], tile] = {}
        self.moves: Dict[Tuple[int, int], move] = {}

    def to_dict(self) -> dict:
        return {
            #"dictMoves": {f"{x},{y}": v.to_dict() for (x, y), v in self.dictMoves.items()},
            # "moves": {f"{x},{y}": v.to_dict() for (x, y), v in self.moves.items()},
            "players": [player.to_dict() for player in self.players]
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

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

        index = len(self.moves)

        if (index >= len(self.tiles)):
            return None

        return self.tiles[index]

    def getMove(self, point: point) -> move | None:
        return self.moves.get((point.x, point.y))

    def getTile(self, x: int, y: int) -> tile | None:
        move = self.getMove(point(x, y))
        
        return move.tile if move else None

    def canPlaceTile(self, x: int, y: int, tile: tile) -> bool:
        if (not self.moves):
            return True

        move = self.getMove(point(x, y))

        if move is not None:
            return False

        for direction, (nx, ny), opposite in self.getNeighbors(x, y):
            neighbor = self.getTile(nx, ny)

            if neighbor is None:
                continue

            edge = tile.edge(direction)
            neighborEdge = neighbor.edge(opposite)

            if edge != neighborEdge:
                return False

        return True

    def placeTile(self, x: int, y: int, tile: tile) -> bool:
        if not self.canPlaceTile(x, y, tile):
            return False

        player = self.getCurrentPlayer()

        tile.setPlayer(player)

        self.dictMoves[(x, y)] = tile
        self.moves[(x, y)] = move(player, tile, point(x, y), tile.rotation)

        return True

    def getAvailablePositions(self) -> list[tuple[int, int]]:
        positions = set()

        if not self.moves:
            return [(0, 0)]

        for (x, y) in self.moves.keys():
            for direction, (nx, ny), _ in self.getNeighbors(x, y):
                if (nx, ny) not in self.moves:
                    positions.add((nx, ny))

        return positions

    def getNeighbors(self, x: int, y: int):
        yield (tileDirection.N, (x, y - 1), tileDirection.S)
        yield (tileDirection.E, (x + 1, y), tileDirection.W)
        yield (tileDirection.S, (x, y + 1), tileDirection.N)
        yield (tileDirection.W, (x - 1, y), tileDirection.E)

    def drawToLog(self):
        """Draws a detailed ASCII map of the board to the logs, showing tile edges and rotation."""
        if not self.moves:
            logging.info("Board is empty.")
            return

        min_x = min(x for x, y in self.moves)
        max_x = max(x for x, y in self.moves)
        min_y = min(y for x, y in self.moves)
        max_y = max(y for x, y in self.moves)

        def color_for_edge(e):
            # Map edge types to colors
            if not COLORAMA_AVAILABLE:
                return lambda ch: ch

            mapping = {
                'CITY': Fore.RED,
                'ROAD': Fore.YELLOW,
                'FIELD': Fore.GREEN,
                'MONASTERY': Fore.MAGENTA,
                '_': Style.DIM,
            }

            def _color(ch, e=e):
                key = getattr(e, 'name', str(e)) if e else '_'
                col = mapping.get(key, '')
                return f"{col}{ch}{Style.RESET_ALL}" if col else ch

            return _color

        def safe_edge_short(t, direction):
            try:
                e = t.edge(direction)
                ch = t.edgeName(direction)
                colorizer = color_for_edge(e)
                return colorizer(ch)
            except Exception:
                colorizer = color_for_edge(None)
                return colorizer("_")

        rows = []
        cols = max_x - min_x + 1

        for y in range(min_y, max_y + 1):
            top_parts = []
            mid_parts = []
            bot_parts = []
            for x in range(min_x, max_x + 1):
                t = self.dictMoves.get((x, y))
                if t:
                    # Special-case tile at (0,0): render whole tile in red (if available)
                    if COLORAMA_AVAILABLE and x == 0 and y == 0:
                        # use raw single-character markers (no per-edge color)
                        n_raw = t.edgeName(tileDirection.N)
                        e_raw = t.edgeName(tileDirection.E)
                        s_raw = t.edgeName(tileDirection.S)
                        w_raw = t.edgeName(tileDirection.W)

                        # Highlight using a bright background so it stands out in logs.
                        highlight_prefix = f"{Back.YELLOW}{Style.BRIGHT}{Fore.BLACK}"
                        highlight_suffix = Style.RESET_ALL

                        top_parts.append(
                            f"{highlight_prefix}*{n_raw}*{highlight_suffix}")
                        mid_parts.append(
                            f"{highlight_prefix}{w_raw}*{e_raw}{highlight_suffix}")
                        bot_parts.append(
                            f"{highlight_prefix}*{s_raw}*{highlight_suffix}")
                    else:
                        n = safe_edge_short(t, tileDirection.N)
                        e = safe_edge_short(t, tileDirection.E)
                        s = safe_edge_short(t, tileDirection.S)
                        w = safe_edge_short(t, tileDirection.W)
                        c = safe_edge_short(t, tileDirection.C)

                        # Format per user request:
                        # *N*
                        # W*E
                        # *S*
                        top_parts.append(f" {n} ")
                        mid_parts.append(f"{w}{c}{e}")
                        bot_parts.append(f" {s} ")
                else:
                    top_parts.append("   ")
                    mid_parts.append("   ")
                    bot_parts.append("   ")

            # join columns with a vertical '|' separator
            top = '|'.join(top_parts)
            mid = '|'.join(mid_parts)
            bot = '|'.join(bot_parts)

            rows.append(top)
            rows.append(mid)
            rows.append(bot)

            if y != max_y:
                sep_len = cols * 3 + (cols - 1) * 1
                rows.append('-' * sep_len)

        board_str = '\n'.join(rows)
        logging.info(
            "\n--------------------------------------------------------------------\n%s", board_str)
