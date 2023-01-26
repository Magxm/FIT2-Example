from Vector2 import Vector2
import pyxel
import Config


class Camera:
    def __init__(self, level):
        self.level = level
        self.maxX = level.tileWidth * Config.TILE_PIXEL_SIZE
        self.maxY = level.tileHeight * Config.TILE_PIXEL_SIZE
        self.location = Vector2(self.maxX / 2, self.maxY / 2)

    def update(self, player):
        self.location = Vector2(player.location)

    def getRelativeDrawPosition(self, location: Vector2, force=False):
        # Calculating where on screen this position is relative to the camera pos (1 pixel is one cell)
        dstX = location.X - self.location.X
        dstY = location.Y - self.location.Y
        drawX = dstX + (Config.SCREEN_WIDTH / 2)
        drawY = dstY + (Config.SCREEN_HEIGHT / 2)
        # Drawing a bit outside of the screen  as well
        if not force and drawX < -Config.TILE_PIXEL_SIZE:
            return None
        elif not force and drawX > Config.SCREEN_WIDTH + Config.TILE_PIXEL_SIZE:
            return None
        elif not force and drawY < -Config.TILE_PIXEL_SIZE:
            return None
        elif not force and drawY > Config.SCREEN_HEIGHT + Config.TILE_PIXEL_SIZE:
            return None
        else:
            return Vector2(drawX, drawY)
