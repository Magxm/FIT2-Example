from Actor.Actor import Actor
from Actor.Monster import Monster
import pyxel
import ResourceHelper
from Vector2 import Vector2
import Map.Helper as Helper


class Player(Actor):
    def __init__(self):
        super().__init__()

        self.movementSpeed = 3
        self.attackSpeed = 6
        self.attackDamage = 30
        self.lastDirection = Vector2(1, 0)

    def update(self, level):
        stepSpeed = self.movementSpeed
        mX = 0
        mY = 0
        if pyxel.btn(pyxel.KEY_A):
            mX -= stepSpeed
        if pyxel.btn(pyxel.KEY_D):
            mX += stepSpeed
        if pyxel.btn(pyxel.KEY_W):
            mY -= stepSpeed
        if pyxel.btn(pyxel.KEY_S):
            mY += stepSpeed

        if (mX != 0 or mY != 0):
            self.move(mX, mY, level)
            self.lastDirection = Vector2(mX, mY)

        if pyxel.btn(pyxel.KEY_SPACE):
            self.attack(Helper.GetMouseLocation(
                level.camera) - self.location, level)

        super().update(level)

    def isEnemy(self, other):
        return type(other) == Monster

    def draw(self, camera):
        location = Vector2(self.location)
        location.X -= 8
        location.Y -= 8
        drawLoc = camera.getRelativeDrawPosition(location)
        if drawLoc is not None:
            ResourceHelper.DrawPlayer(drawLoc, self.lastForward)
            super().draw(camera)

        # Draw HP bar
        pyxel.rect(20, pyxel.height - 30, 200, 20, pyxel.COLOR_BLACK)
        pyxel.rect(20, pyxel.height - 30, 200 *
                   (self.hp / self.maxHP), 20, pyxel.COLOR_RED)
        pyxel.text(100, pyxel.height - 38,
                   f"{int(self.hp)} / {int(self.maxHP)}", pyxel.COLOR_WHITE)
