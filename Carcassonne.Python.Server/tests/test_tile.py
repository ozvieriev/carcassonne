import pytest

from proj.game.factories import *
from proj.game.models import *
from proj.game.enums import *

def test_createTileReturnsTile():
    createdTile = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert isinstance(createdTile, tile)


def test_createTileEdgesAreCorrect():
    createdTile = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)

    assert createdTile.edge(tileDirection.N) == tileEdge.CITY
    assert createdTile.edge(tileDirection.E) == tileEdge.ROAD
    assert createdTile.edge(tileDirection.S) == tileEdge.FIELD
    assert createdTile.edge(tileDirection.W) == tileEdge.ROAD


def test_createTileEdgesAreCorrectRotated():
    createdTile = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)

    createdTile.rotate()

    assert createdTile.edge(tileDirection.N) == tileEdge.ROAD
    assert createdTile.edge(tileDirection.E) == tileEdge.CITY
    assert createdTile.edge(tileDirection.S) == tileEdge.ROAD
    assert createdTile.edge(tileDirection.W) == tileEdge.FIELD

    createdTile.rotate()

    assert createdTile.edge(tileDirection.N) == tileEdge.FIELD
    assert createdTile.edge(tileDirection.E) == tileEdge.ROAD
    assert createdTile.edge(tileDirection.S) == tileEdge.CITY
    assert createdTile.edge(tileDirection.W) == tileEdge.ROAD

    createdTile.rotate()

    assert createdTile.edge(tileDirection.N) == tileEdge.ROAD
    assert createdTile.edge(tileDirection.E) == tileEdge.FIELD
    assert createdTile.edge(tileDirection.S) == tileEdge.ROAD
    assert createdTile.edge(tileDirection.W) == tileEdge.CITY

    createdTile.rotate()

    assert createdTile.edge(tileDirection.N) == tileEdge.CITY
    assert createdTile.edge(tileDirection.E) == tileEdge.ROAD
    assert createdTile.edge(tileDirection.S) == tileEdge.FIELD
    assert createdTile.edge(tileDirection.W) == tileEdge.ROAD

def test_tileRotationChangesRotationValue():
    createdTile = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)

    assert createdTile.rotation == 0
    assert createdTile.rotate() == 90
    assert createdTile.rotate() == 180
    assert createdTile.rotate() == 270
    assert createdTile.rotate() == 0
