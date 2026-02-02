import logging
from proj.core.factories import *
from proj.core.models import *
from proj.core.enums import *


def testCreateTileReturnsTile():
    createdTile = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)
    assert isinstance(createdTile, tile)


def testCreateTileEdgesAreCorrect():
    createdTile = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)

    assert createdTile.edge(tileDirection.N) == tileEdge.CITY
    assert createdTile.edge(tileDirection.E) == tileEdge.ROAD
    assert createdTile.edge(tileDirection.S) == tileEdge.FIELD
    assert createdTile.edge(tileDirection.W) == tileEdge.ROAD


def testCreateTileEdgesAreCorrectRotated():
    createdTile = tileFactory.createTile(
        tileEdge.CITY, tileEdge.ROAD, tileEdge.FIELD, tileEdge.ROAD)

    assert createdTile.edge(tileDirection.N) == tileEdge.CITY
    assert createdTile.edge(tileDirection.E) == tileEdge.ROAD
    assert createdTile.edge(tileDirection.S) == tileEdge.FIELD
    assert createdTile.edge(tileDirection.W) == tileEdge.ROAD

    assert createdTile.edge(tileDirection.N, tileRotation.R90) == tileEdge.ROAD
    assert createdTile.edge(tileDirection.E, tileRotation.R90) == tileEdge.CITY
    assert createdTile.edge(tileDirection.S, tileRotation.R90) == tileEdge.ROAD
    assert createdTile.edge(tileDirection.W, tileRotation.R90) == tileEdge.FIELD

    assert createdTile.edge(tileDirection.N, tileRotation.R180) == tileEdge.FIELD
    assert createdTile.edge(tileDirection.E, tileRotation.R180) == tileEdge.ROAD
    assert createdTile.edge(tileDirection.S, tileRotation.R180) == tileEdge.CITY
    assert createdTile.edge(tileDirection.W, tileRotation.R180) == tileEdge.ROAD

    assert createdTile.edge(tileDirection.N, tileRotation.R270) == tileEdge.ROAD
    assert createdTile.edge(tileDirection.E, tileRotation.R270) == tileEdge.FIELD
    assert createdTile.edge(tileDirection.S, tileRotation.R270) == tileEdge.ROAD
    assert createdTile.edge(tileDirection.W, tileRotation.R270) == tileEdge.CITY


def testTileLoadFromMap():

    tiles = tileFactory.loadFromMap()

    assert len(tiles) > 0
