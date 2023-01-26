from Map.Tile import Tile
from Map.TilePresets.FloorTile import FloorTile
import random
import math
import Map.Helper as Helper
import ResourceHelper
from Vector2 import Vector2
from Camera import Camera
import Config


class WallTile(Tile):
    def __init__(self, tX, tY):
        super().__init__(tX, tY)
        self.walkable = False
        self.isWallTile = True

    def draw(self, camera: Camera, level):
        location = Helper.TileToLocation(Vector2(self.tX, self.tY))
        location.X -= Config.TILE_PIXEL_SIZE / 2
        location.Y -= Config.TILE_PIXEL_SIZE / 2

        drawLoc = camera.getRelativeDrawPosition(location)

        # check which wall we have to render
        tileAbove = level.getTile(self.tX, self.tY - 1)
        tileRight = level.getTile(self.tX + 1, self.tY)
        tileLeft = level.getTile(self.tX - 1, self.tY)
        tileDown = level.getTile(self.tX, self.tY + 1)
        wallAbove = tileAbove is not None and tileAbove.isWallTile
        wallRight = tileRight is not None and tileRight.isWallTile
        wallLeft = tileLeft is not None and tileLeft.isWallTile
        wallDown = tileDown is not None and tileDown.isWallTile
        walkableDown = tileDown is not None and tileDown.walkable
        walkableRight = tileRight is not None and tileRight.walkable
        walkableAbove = tileAbove is not None and tileAbove.walkable

        index = 0
        if walkableDown:
            if wallRight and wallLeft:
                if not wallAbove:
                    index = 1
                else:
                    index = 2
            elif wallRight:
                if wallDown:
                    if wallAbove:
                        index = 3
                    else:
                        index = 4
                else:
                    if walkableRight:
                        index = 8
                    else:
                        index = 10
            else:
                if wallLeft and wallAbove:
                    if walkableRight:
                        index = 2
                    else:
                        index = 11
                elif walkableRight:
                    index = 7
                elif walkableDown:
                    index = 1
        else:
            if wallAbove:
                if wallDown:
                    if not wallRight:
                        index = 5
                    else:
                        index = 12
                else:
                    if wallRight:
                        index = 3
                    elif walkableRight:
                        index = 5
                    else:
                        # No need for a wall
                        return
            else:
                if wallDown:
                    if walkableRight and walkableAbove:
                        index = 6
                    elif wallRight:
                        index = 9
                else:
                    if walkableAbove and walkableRight:
                        index = 13

        if drawLoc is not None:
            # super().draw_ifWalkable(camera)
            ResourceHelper.DrawWallTile(drawLoc, index)

    def load(self):
        pass
