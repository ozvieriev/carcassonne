from proj.core.factories import *
from proj.core.services import *
from proj.core.models import *
from proj.core.enums import *
from proj.core.factories.playerFactory import playerFactory
import time


def testPlaceInitialTile():
    players = playerFactory.loadFromMap()
    b = board(players, tileFactory.loadFromMap())
    t = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, t)


def testCannotPlaceOnOccupied():
    players = playerFactory.loadFromMap()
    b = board(players, tileFactory.loadFromMap())
    t = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, t)
    # placing another tile at the same coordinates should fail
    t2 = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.ROAD, tileEdge.ROAD, tileEdge.FIELD)
    assert b.placeTile(0, 0, t2) is False


def testCanPlaceAdjacentMatching():
    players = playerFactory.loadFromMap()
    b = board(players, tileFactory.loadFromMap())
    base = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, base)

    # base north is CITY, so a tile placed at (0, -1) must have south == CITY
    matching = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.ROAD, tileEdge.CITY, tileEdge.ROAD)
    assert b.placeTile(0, -1, matching)


def testRejectMismatchedAdjacent():
    players = playerFactory.loadFromMap()
    b = board(players, tileFactory.loadFromMap())
    base = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, base)

    # base north is CITY; provide a tile whose south is not CITY
    bad = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.ROAD, tileEdge.ROAD, tileEdge.FIELD)
    assert b.placeTile(0, -1, bad) is False


def testRotationAwarePlacement():
    players = playerFactory.loadFromMap()
    b = board(players, tileFactory.loadFromMap())
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


def testAvailablePositions(request):

    players = playerFactory.loadFromMap()
    b = board(players, tileFactory.loadFromMap())
    r = renderService(b)
    htmlS = htmlService()

    t = b.getNextTile()

    assert b.placeTile(0, 0, t)

    htmlS.saveToFile(request.node.name, r.toHtml())

    t = b.getNextTile()
    while t is not None:
        positions = b.getAvailablePositions()

        if len(positions) == 0:
            break

        for position in positions:
            rotation = t.rotation

            while (placed := b.placeTile(position[0], position[1], t)) is False:

                if (placed):
                    htmlS.saveToFile(request.node.name, r.toHtml())

                if rotation == t.rotate():
                    break

        t = b.getNextTile()

    s = r.toJson()

    assert 'players' in s

    with open("proj/core/data/output/board.json", "w") as write:
        json.dump(b.to_dict(), write, indent=4, ensure_ascii=False)
    
    #htmlS.saveToFile(request.node.name, r.toHtml())

def testAddAndGetPlayers():
    players = playerFactory.loadFromMap()
    # take two players from the factory (or fewer if file smaller)
    selected = players[:2]

    p1 = players[0]
    p2 = players[1]

    b = board(selected, tileFactory.loadFromMap())

    players = b.getPlayers()
    assert len(players) == 2
    assert players[0] is p1
    assert players[1] is p2

    # current player should be first added
    assert b.getCurrentPlayer() is p1


def testAddPlayers():
    players = playerFactory.loadFromMap()
    # take three players from the factory (or fewer if file smaller)
    selected = players[:3]

    # pass the full factory players list per test conventions
    b = board(selected, tileFactory.loadFromMap())

    got = b.getPlayers()
    assert len(got) == len(selected)
    # order should be preserved
    for i in range(len(selected)):
        assert got[i] is selected[i]

    # first added becomes current player
    if len(selected) > 0:
        assert b.getCurrentPlayer() is selected[0]


def testPlaceTileAdvancesPlayer():
    players = playerFactory.loadFromMap()
    # take two players from the factory (or fewer if file smaller)
    selected = players[:2]
    p1 = players[0]
    p2 = players[1]

    b = board(selected, tileFactory.loadFromMap())

    # starting player
    assert b.getCurrentPlayer() is p1

    # placing a tile should advance to next player
    t = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, t)
    assert b.getCurrentPlayer() is p2


def testTilePlacementRecordsOwner():
    players = playerFactory.loadFromMap()
    # take two players from the factory (or fewer if file smaller)
    selected = players[:2]
    p1 = players[0]
    p2 = players[1]

    b = board(selected, tileFactory.loadFromMap())

    # first player places at (0,0)
    t1 = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(0, 0, t1)

    # next player places at (1,0) using a tile that rotates to match west==ROAD
    t2 = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.FIELD, tileEdge.ROAD, tileEdge.FIELD)
    t2.rotate()
    assert b.placeTile(1, 0, t2)
    assert b.getTile(1, 0).playerId == p2.id
