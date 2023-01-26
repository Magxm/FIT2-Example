from Map.Pathfinder import PathfinderNode
from Vector2 import Vector2
import Config
import pyxel
import Map.Helper as Helper


class Tile(PathfinderNode):
    def __init__(self, tX, tY, walkable=True):
        super().__init__()
        self.tX = int(tX)
        self.tY = int(tY)
        self.tilePos = Vector2(tX, tY)
        self.tile = None
        self.walkable = walkable
        self.isWallTile = False

    def draw(self, camera, level):
        pass

    def draw_ifWalkable(self, camera):
        if self.walkable:
            location = Helper.TileToLocation(Vector2(self.tX, self.tY))
            location.X -= Config.TILE_PIXEL_SIZE / 2
            location.Y -= Config.TILE_PIXEL_SIZE / 2

            drawLoc = camera.getRelativeDrawPosition(location)
            if drawLoc is not None:
                pyxel.rect(drawLoc.X - 1, drawLoc.Y - 1, Config.TILE_PIXEL_SIZE + 2,
                           Config.TILE_PIXEL_SIZE + 2, 8)

    def getHeuristic(self, other):
        dx = abs(self.tX - other.tX)
        dy = abs(self.tY - other.tY)
        return 1.1 * (dx + dy)

    def getMovementCost(self, other):
        # If diagonal movement, then 1.3, else 1
        if (self.tX != other.tX and self.tY != other.tY):
            return 1.3
        return 1

    def load(self):
        pass
