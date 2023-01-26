from matplotlib.pyplot import draw
from Vector2 import Vector2
import pyxel


class Stair:
    def __init__(self):
        self.location = Vector2()

    def draw(self, camera):
        drawLoc = camera.getRelativeDrawPosition(self.location)
        if drawLoc is not None:
            pyxel.blt(drawLoc.X-8, drawLoc.Y-8, 0, 0, 48, 16, 16, 3)
