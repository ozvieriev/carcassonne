class color:
    def __init__(self, name: str, hex: str):
        self.name = name
        self.hex = hex

    @classmethod
    def from_dict(self, data: dict):
        name = data.get("name", "Black")
        hex = data.get("hex", "#000")

        return self(name, hex)
