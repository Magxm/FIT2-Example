from Config import TILE_PIXEL_SIZE
from Vector2 import Vector2
import Config
import Map.Helper as Helper


class Room:
    def __init__(self, centerTilePos: Vector2, tileWidth: int, tileHeight: int):
        # A room is a square containing x tiles
        self.tiles = []
        self.centerTilePos = centerTilePos
        self.center = Helper.TileToLocation(centerTilePos)
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.cellWidth = tileWidth * Config.TILE_PIXEL_SIZE
        self.cellHeight = tileHeight * Config.TILE_PIXEL_SIZE

    def load(self):
        for tile in self.tiles:
            tile.load()

    def getTiles(self):
        return self.tiles

    def calculateTopLeftTilePos(self):
        return self.centerTilePos - Vector2(self.tileWidth / 2, self.tileHeight / 2)

    def getCorner(self, index):
        if index == 0:
            # Top left
            return Vector2(self.center + Vector2(-self.cellWidth / 2, -self.cellHeight / 2))
        elif index == 1:
            # Top right
            return Vector2(self.center + Vector2(self.cellWidth / 2, -self.cellHeight / 2))
        elif index == 2:
            # Bottom right
            return Vector2(self.center + Vector2(self.cellWidth / 2, self.cellHeight / 2))
        elif index == 3:
            # Bottom left
            return Vector2(self.center + Vector2(-self.cellWidth / 2, self.cellHeight / 2))
