import json
from proj.core.models import *
from proj.core.factories.playerFactory import playerFactory


def testColorFromDictWithHex():
    data = {"name": "Red", "hex": "#FF0000"}
    c = color.from_dict(data)

    assert isinstance(c, color)
    assert c.name == "Red"
    assert c.hex == "#FF0000"


def testColorFromDictWithMissingFields():
    c = color.from_dict({})

    assert isinstance(c, color)
    assert c.name == "Black"
    assert c.hex == "#000"


def testPlayerFromDictUsesColorFromDict():
    players = playerFactory.loadFromMap()
    assert isinstance(players, list)
    assert len(players) > 0

    p = players[0]
    assert isinstance(p, player)
    assert p.name == "Alice"
    assert isinstance(p.color, color)
    assert p.color.name == "Red"
    assert p.color.hex == "#f00"


def testCreatePlayerReturnsPlayer():
    players = playerFactory.loadFromMap()
    # pick second player (Bob)
    assert len(players) > 1
    p = players[1]

    assert isinstance(p, player)
    assert p.name == "Bob"
    assert isinstance(p.color, color)
