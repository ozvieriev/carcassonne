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
    #return client.put(path, **kwargs)

def testPlay(request):
    
    response = put("/game/")
    assert response.status_code == 200

    json = response.json()

    d = dict(json)
    gameId = d.get("id", "")
    
    webbrowser.open(BASE_URL + "/?gameId=" + gameId)
    
    dataNextTile = d.get("nextTile", {})
    dataAvailablePositions = d.get("availablePositions", [])

    while(t := tile.from_dict(dataNextTile) if dataNextTile is not None else None) is not None:
        positions = [point.from_dict(p) for p in dataAvailablePositions]

        if len(positions) == 0:
            assert False, "No available positions to place tile" #TODO

        for position in positions:
            rotation = tileRotation.R0

            while True :
                try:
                    request = {
                        "location": position.to_dict(),
                        "rotation": rotation.value
                    }
                    response = put(f"/game/{gameId}/placeTile", json=request)

                    if(response.status_code == 200):
                        json = response.json()

                        d = dict(json)

                        dataNextTile = d.get("nextTile", {})
                        dataAvailablePositions = d.get("availablePositions", [])
                    else:
                        pass

                finally:
                    pass

                rotation = rotation.rotate()

                if rotation == tileRotation.R0 or response.status_code == 200:
                    break
            
            if rotation == tileRotation.R0 or response.status_code == 200:
                break
                

