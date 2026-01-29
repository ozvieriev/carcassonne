from ..models.tile import tile, tileEdge, tileDirection


class tileFactory:
    @staticmethod
    def createTile(north: tileEdge, east: tileEdge, south: tileEdge, west: tileEdge, center: tileEdge = None) -> tile:
        edges = {
            tileDirection.N: north,
            tileDirection.E: east,
            tileDirection.S: south,
            tileDirection.W: west,
            tileDirection.C: center
        }

        return tile(edges)