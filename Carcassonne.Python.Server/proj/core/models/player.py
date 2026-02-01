from .color import color

class player:
    def __init__(self, name: str, color: color):
        self.name = name
        self.color = color

    def to_dict(self) -> dict:
        return {
            "name": self.name,
        }

    @classmethod
    def from_dict(self, data: dict):
        name = data.get("name", "")
        _color = color.from_dict(data.get("color", {}))

        return self(name, _color)