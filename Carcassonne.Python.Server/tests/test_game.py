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
    assert b.placeTile(0, 0, t)

    while (t := b.getNextTile()) is not None:
        placed = False
        positions = b.getAvailablePositions(t)
        #htmlS.saveToFile(request.node.name, r.toHtml(t))  

        if len(positions) == 0:
           assert False, "No available positions to place tile" #TODO

        for position in positions:
            rotation = tileRotation.R0

            while (placed := b.placeTile(position[0], position[1], t, rotation)) is False:
                rotation = rotation.rotate()

                if rotation == tileRotation.R0:
                    break

            # if (placed):
            #     htmlS.saveToFile(request.node.name, r.toHtml())
            #     break

    s = r.toJson()

    assert 'players' in s

    with open("proj/core/data/output/board.json", "w") as write:
        json.dump(b.to_dict(), write, indent=4, ensure_ascii=False)

    htmlS.saveToFile(request.node.name, r.toHtml())