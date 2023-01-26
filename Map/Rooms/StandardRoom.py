from Map.Room import Room
import random
from Map.TilePresets.FloorTile import FloorTile
from Map.TilePresets.WallTile import WallTile
from Vector2 import Vector2


class StandardRoom(Room):
    def __init__(self, center: Vector2, tileWidth: int, tileHeight: int):
        super().__init__(center, tileWidth, tileHeight)
        # We create the tiles array and fill it will tiles
        self.tiles = []
        tileOffset = self.calculateTopLeftTilePos()
        for tX in range(tileWidth):
            for tY in range(tileHeight):
                self.tiles.append(
                    FloorTile(int(tileOffset.X + tX), int(tileOffset.Y + tY)))
