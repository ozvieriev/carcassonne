from proj.game.factories import *
from proj.game.models import *
from proj.game.enums import *


def test_placeInitialTile():
    b = board()
    t = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, t)


def test_cannotPlaceOnOccupied():
    b = board()
    t = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, t)
    # placing another tile at the same coordinates should fail
    t2 = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.ROAD, tileEdge.ROAD, tileEdge.FIELD)
    assert b.placeTile(0, 0, t2) is False


def test_canPlaceAdjacentMatching():
    b = board()
    base = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, base)

    # base north is CITY, so a tile placed at (0, -1) must have south == CITY
    matching = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.ROAD, tileEdge.CITY, tileEdge.ROAD)
    assert b.placeTile(0, -1, matching)


def test_rejectMismatchedAdjacent():
    b = board()
    base = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, base)

    # base north is CITY; provide a tile whose south is not CITY
    bad = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.ROAD, tileEdge.ROAD, tileEdge.FIELD)
    assert b.placeTile(0, -1, bad) is False


def test_rotationAwarePlacement():
    b = board()
    t = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, t)

    # base east is ROAD, so tile at (1,0) must have west == ROAD
    # create a tile whose south == ROAD, and rotate it so south moves to west
    rot_tile = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.FIELD, tileEdge.ROAD, tileEdge.FIELD)
    # after one 90-degree clockwise rotation, the edge in the west position will be original south
    rot_tile.rotate()
    assert rot_tile.rotation == 90
    assert b.placeTile(1, 0, rot_tile)


def test_MapTilePlacement():
    b = board()
    tiles = tileFactory.loadFromMap()
    t = tiles.pop()

    assert b.placeTile(0, 0, t)

    # while len(tiles) > 0:
    #     t = tiles.pop()
    #     assert b.placeTile(0, 0, t)


def test_availablePositions():
    b = board()
    tiles = tileFactory.loadFromMap()
    t = tiles.pop()

    assert b.placeTile(0, 0, t)

    while len(tiles) > 0:
        positions = b.availablePositions()

        if len(positions) == 0:
            break

        t = tiles.pop()

        for position in positions:
            rotation = t.rotation

            while (placed := b.placeTile(position[0], position[1], t)) is False:
                if rotation == t.rotate():
                    break
            
            if placed:
                break
    
    assert len(tiles) == 0
