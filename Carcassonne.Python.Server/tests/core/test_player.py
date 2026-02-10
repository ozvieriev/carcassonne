import json
from proj.core.models import *
from proj.core.factories.playerFactory import playerFactory

def testPlayerFromDictUsesColorFromDict():
    players = playerFactory.loadFromMap()
    assert isinstance(players, list)
    assert len(players) > 0

    p = players[0]
    assert isinstance(p, player)
    

def testCreatePlayerReturnsPlayer():
    players = playerFactory.loadFromMap()
    # pick second player (Bob)
    assert len(players) > 1
    p = players[1]

    assert isinstance(p, player)