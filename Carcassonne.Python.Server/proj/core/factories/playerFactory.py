from ..models.player import player
import json, random

class playerFactory:
    @staticmethod
    def loadFromMap(path: str = "proj/core/data/players.json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        players = [player.from_dict(item) for item in data]
        #random.shuffle(players)

        return players
