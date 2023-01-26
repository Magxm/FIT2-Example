from Map.Tile import Tile
from Map.TilePresets.FloorTile import FloorTile
import random
import math
import Map.Helper as Helper
import ResourceHelper
from Vector2 import Vector2
from Camera import Camera
import Config


class CorridorTile(FloorTile):
    def __init__(self, tX, tY, index=0):
        super().__init__(tX, tY)
        self.tileIndex = index
        self.walkable = True

    def draw(self, camera: Camera, level):
        location = Helper.TileToLocation(Vector2(self.tX, self.tY))
        location.X -= Config.TILE_PIXEL_SIZE / 2
        location.Y -= Config.TILE_PIXEL_SIZE / 2

        drawLoc = camera.getRelativeDrawPosition(location)

        if drawLoc is not None:
            # super().draw_ifWalkable(camera)
            ResourceHelper.DrawCorridorTile(drawLoc)

    def load(self):
        pass
