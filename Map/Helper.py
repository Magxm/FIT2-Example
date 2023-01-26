from Vector2 import Vector2
import Config
import math
import pyxel


def LocationToTile(location):
    return Vector2(int(location.X // Config.TILE_PIXEL_SIZE), int(location.Y // Config.TILE_PIXEL_SIZE))


def TileToLocation(location):
    return Vector2(int(location.X * Config.TILE_PIXEL_SIZE + Config.TILE_PIXEL_SIZE/2), int(location.Y * Config.TILE_PIXEL_SIZE + Config.TILE_PIXEL_SIZE/2))


def GetMouseLocation(camera):
    mouseX = pyxel.mouse_x + \
        camera.location.X - (pyxel.width / 2)
    mouseY = pyxel.mouse_y + \
        camera.location.Y - (pyxel.height / 2)

    return Vector2(mouseX, mouseY)
