from proj.core.factories import *
from proj.core.models import *
from proj.core.enums import *
from proj.core.factories.playerFactory import playerFactory


def testPlaceInitialTile():
    b = board()
    t = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, t)


def testCannotPlaceOnOccupied():
    b = board()
    t = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, t)
    # placing another tile at the same coordinates should fail
    t2 = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.ROAD, tileEdge.ROAD, tileEdge.FIELD)
    assert b.placeTile(0, 0, t2) is False


def testCanPlaceAdjacentMatching():
    b = board()
    base = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, base)

    # base north is CITY, so a tile placed at (0, -1) must have south == CITY
    matching = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.ROAD, tileEdge.CITY, tileEdge.ROAD)
    assert b.placeTile(0, -1, matching)


def testRejectMismatchedAdjacent():
    b = board()
    base = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, base)

    # base north is CITY; provide a tile whose south is not CITY
    bad = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.ROAD, tileEdge.ROAD, tileEdge.FIELD)
    assert b.placeTile(0, -1, bad) is False


def testRotationAwarePlacement():
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

def testAvailablePositions():
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
                b.drawToLog()
                break
    
    assert len(tiles) == 0

    

def testAddAndGetPlayers():
    b = board()

    players = playerFactory.loadFromMap()
    p1 = players[0]
    p2 = players[1]

    b.addPlayer(p1)
    b.addPlayer(p2)

    players = b.getPlayers()
    assert len(players) == 2
    assert players[0] is p1
    assert players[1] is p2

    # current player should be first added
    assert b.currentPlayer() is p1


def testAddPlayers():
    b = board()

    players = playerFactory.loadFromMap()
    # take three players from the factory (or fewer if file smaller)
    selected = players[:3]

    b.addPlayers(selected)

    got = b.getPlayers()
    assert len(got) == len(selected)
    # order should be preserved
    for i in range(len(selected)):
        assert got[i] is selected[i]

    # first added becomes current player
    if len(selected) > 0:
        assert b.currentPlayer() is selected[0]


def testNextPlayerWrapsAround():
    b = board()

    players = playerFactory.loadFromMap()
    p1 = players[0]
    p2 = players[1]
    p3 = players[2]

    b.addPlayer(p1)
    b.addPlayer(p2)
    b.addPlayer(p3)

    assert b.currentPlayer() is p1
    assert b.nextPlayer() is p2
    assert b.nextPlayer() is p3
    # wrap back to first
    assert b.nextPlayer() is p1

def testPlaceTileAdvancesPlayer():
    b = board()

    players = playerFactory.loadFromMap()
    p1 = players[0]
    p2 = players[1]

    b.addPlayers([p1, p2])

    # starting player
    assert b.currentPlayer() is p1

    # placing a tile should advance to next player
    t = tileFactory.createTile(tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, t)
    assert b.currentPlayer() is p2


def testTilePlacementRecordsOwner():
    b = board()

    players = playerFactory.loadFromMap()
    p1 = players[0]
    p2 = players[1]

    b.addPlayers([p1, p2])

    # first player places at (0,0)
    t1 = tileFactory.createTile(tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, t1)

    # next player places at (1,0) using a tile that rotates to match west==ROAD
    t2 = tileFactory.createTile(tileEdge.FIELD, tileEdge.FIELD, tileEdge.ROAD, tileEdge.FIELD)
    t2.rotate()
    assert b.placeTile(1, 0, t2)
    assert b.getTile(1, 0).player is p2


