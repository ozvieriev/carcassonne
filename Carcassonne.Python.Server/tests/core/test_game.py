from proj.core.factories import *
from proj.core.services import *
from proj.core.models import *
from proj.core.enums import *
from proj.core.factories.playerFactory import playerFactory
from time import sleep


def testPlay(request):

    players = playerFactory.loadFromMap()
    b = board(players, tileFactory.loadFromMap())
    r = renderService(b)
    htmlS = htmlService()

    t = b.getNextTile()
    assert b.placeTile(point(0, 0), t)

    while (t := b.getNextTile()) is not None:
        nextMove = b.getAnyAvailableMove(t)
        htmlS.saveToFile(request.node.name, r.toHtml(t))  

        if not nextMove:
           assert False, "No available positions to place tile" #TODO

        location = nextMove.location
        rotation = nextMove.rotations[0]

        placed = b.placeTile(location, t, rotation)
        assert placed, "Failed to place tile at " + str(location) + " with rotation " + str(rotation)

    s = r.toJson()

    assert 'players' in s

    with open("proj/core/data/output/board.json", "w") as write:
        json.dump(b.to_dict(), write, indent=4, ensure_ascii=False)

    htmlS.saveToFile(request.node.name, r.toHtml())