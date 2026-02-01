class player:
    def __init__(self, id: str, name: str, color: str):
        self.id = id
        self.name = name
        self.color = color

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color
        }

    @classmethod
    def from_dict(self, data: dict):
        id = data.get("id", "")
        name = data.get("name", "")
        color = data.get("color", "")

        return self(id, name, color)