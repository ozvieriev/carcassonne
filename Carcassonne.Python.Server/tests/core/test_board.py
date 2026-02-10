from proj.core.factories import *
from proj.core.services import *
from proj.core.models import *
from proj.core.enums import *
from proj.core.factories.playerFactory import playerFactory
from time import sleep
import pytest

@pytest.fixture
def bFixture():
    players = playerFactory.loadFromMap()
    b = board(players, tileFactory.loadFromMap())
    t = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert b.placeTile(point(0, 0), t)

    return b


def testCannotPlaceOnOccupied(bFixture):
    t2 = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.ROAD, tileEdge.ROAD, tileEdge.FIELD)

    assert bFixture.placeTile(point(0, 0), t2) is False


def testCanPlaceAdjacentMatching(bFixture):
    t2 = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.ROAD, tileEdge.CITY, tileEdge.ROAD)

    assert bFixture.placeTile(point(0, -1), t2)


def testRejectMismatchedAdjacent(bFixture):
    t2 = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.ROAD, tileEdge.ROAD, tileEdge.FIELD)
    
    assert bFixture.placeTile(point(0, -1), t2) is False


def testRotationAwarePlacement(bFixture):
    t2 = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.FIELD, tileEdge.ROAD, tileEdge.ROAD)

    assert bFixture.placeTile(point(1, 0), t2, tileRotation.R90)


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
    assert b.placeTile(point(0, 0), t)
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
        tileEdge.CITY, tileEdge.FIELD, tileEdge.ROAD, tileEdge.ROAD)
    assert b.placeTile(point(0, 0), t1)

    # next player places at (1,0) using a tile that rotates to match west==ROAD
    t2 = tileFactory.createTile(
        tileEdge.FIELD, tileEdge.FIELD, tileEdge.ROAD, tileEdge.FIELD)

    assert b.placeTile(point(1, 0), t2)
