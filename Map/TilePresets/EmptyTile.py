from Map.Tile import Tile


class EmptyTile(Tile):
    def __init__(self, tX, tY):
        super().__init__(tX, tY)
        self.walkable = False

    def draw(self, camera, level):
        pass

    def load(self):
        pass
