from Map.Tile import Tile
import random
import math
import Map.Helper as Helper
import ResourceHelper
from Vector2 import Vector2
from Camera import Camera
import Config
import pyxel


class FloorTile(Tile):
    def __init__(self, tX, tY):
        super().__init__(tX, tY)
        self.walkable = True
        self.index = random.randint(0, 2)
        self.decorationIndex = -1 if random.random() < 0.99 else pyxel.rndi(0, 5)

    def draw(self, camera: Camera, level):
        location = Helper.TileToLocation(Vector2(self.tX, self.tY))
        location.X -= Config.TILE_PIXEL_SIZE / 2
        location.Y -= Config.TILE_PIXEL_SIZE / 2

        drawLoc = camera.getRelativeDrawPosition(location)
        #print(f"Location: {location} \n DrawLoc: {drawLoc} \n ------------")

        if drawLoc is not None:
            # super().draw_ifWalkable(camera)
            ResourceHelper.DrawFloorTile(drawLoc, self.index)
            if self.decorationIndex >= 0:
                ResourceHelper.DrawDecoration(drawLoc, self.decorationIndex)
            # pyxel.text(drawLoc.X, drawLoc.Y, f"{self.tX}", 9)
            # pyxel.text(drawLoc.X, drawLoc.Y + 8, f"{self.tY}", 9)

    def load(self):
        pass
