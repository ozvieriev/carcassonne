from datetime import datetime
import webbrowser

import requests
from proj.api.models import gamePlaceTileRequest
from proj.core.factories import *
from proj.core.services import *
from proj.core.models import *
from proj.core.enums import *
from fastapi.testclient import TestClient
from proj.api import app

BASE_URL = "http://localhost:8000"
client = TestClient(app)


def get(path, **kwargs):
    return client.get(path, **kwargs)


def post(path, **kwargs):
    return client.post(path, **kwargs)


def put(path, **kwargs):
    return requests.put(BASE_URL + path, **kwargs)
    # return client.put(path, **kwargs)


def testPlay(request):

    response = put("/game/")
    assert response.status_code == 200

    json = response.json()

    d = dict(json)
    gameId = d.get("id", "")

    webbrowser.open(BASE_URL + f"/#!/en/game/{gameId}?playerId=alice")

    dataNextTile = d.get("nextTile", {})
    dataAvailableMoves = d.get("availableMoves", [])

    index = 0
    while (t := tile.from_dict(dataNextTile) if dataNextTile is not None else None) is not None:
        nextMove = next(iter([availableMove.from_dict(am) for am in dataAvailableMoves]), None)

        if not nextMove:
            assert False, "No available positions to place tile"  # TODO

        location = nextMove.location
        rotation = next(iter(nextMove.rotations))

        request = {
            "location": location.to_dict(),
            "rotation": rotation.value
        }

        response = put(f"/game/{gameId}/placeTile", json=request)

        if (response.status_code == 200):
            index += 1

            json = response.json()

            d = dict(json)

            dataNextTile = d.get("nextTile", {})
            dataAvailableMoves = d.get("availableMoves", [])
        else:
            assert False, f"Failed to place tile at {location} with rotation {rotation}. Response: {response.text}"
