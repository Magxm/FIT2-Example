from Vector2 import Vector2
import math
import time
import pyxel
import MathUtils


class Actor:
    def __init__(self):
        self.skills = []
        self.maxHP = 100
        self.hp = self.maxHP
        self.location = Vector2()
        self.movementSpeed = 1
        self.lastForward = True
        self.lastAttackTime = 0
        self.attackSpeed = 1
        self.attackDamage = 4
        self.lastAttackLocation = None
        self.lastAttackDirection = 0

        self.vX = 0
        self.vY = 0

    def canAttack(self):
        secondsLeft = (self.lastAttackTime +
                       (3 / self.attackSpeed)) - time.time()
        return secondsLeft <= 0

    def isEnemy(self, other):
        return False

    def push(self, pushVec):
        self.vX = pushVec.X
        self.vY = pushVec.Y

    def handlePotentialAttackTarget(self, enemy, A, B, C, D, pushVectorNormalized):
        if enemy is self:
            return False

        if not self.isEnemy(enemy):
            return False

        if MathUtils.hasCircleRectCollision(enemy.location, 8, [A, B, C, D]):
            enemy.hp -= self.attackDamage
            enemy.push(pushVectorNormalized * 10)
            return True

        return False

    def attack(self, targetDirection, level):
        if not self.canAttack():
            return

        self.lastAttackTime = time.time()
        self.lastAttackLocation = self.location
        rVec = targetDirection.getNormalized()
        # Directions:
        # 0: Up
        # 1: Up Right
        # 2: Right
        # 3: Down Right
        # 4: Down
        # 5: Down Left
        # 6: Left
        # 7: Up Left
        if rVec.Y <= -0.25 and abs(rVec.X) < 0.25:
            self.lastAttackDirection = 0
        elif rVec.X >= 0.25 and rVec.Y <= -0.25:
            self.lastAttackDirection = 1
        elif rVec.X >= 0.25 and abs(rVec.Y) < 0.25:
            self.lastAttackDirection = 2
        elif rVec.X >= 0.25 and rVec.Y > 0.25:
            self.lastAttackDirection = 3
        elif rVec.Y >= 0.25 and abs(rVec.X) < 0.25:
            self.lastAttackDirection = 4
        elif rVec.X <= -0.25 and rVec.Y >= 0.25:
            self.lastAttackDirection = 5
        elif rVec.X <= -0.25 and abs(rVec.Y) < 0.25:
            self.lastAttackDirection = 6
        elif rVec.X <= -0.25 and rVec.Y <= -0.25:
            self.lastAttackDirection = 7
        else:
            print("ERROR: Invalid attack direction calculation")

        # Check what actors we hit with our attack
        endPoint = self.location + (rVec * 24)
        rightAngleVec = Vector2(rVec.Y, -rVec.X) * 12

        A = endPoint + rightAngleVec
        B = endPoint - rightAngleVec
        C = self.location + rightAngleVec
        D = self.location - rightAngleVec

        for enemy in level.enemies:
            self.handlePotentialAttackTarget(enemy, A, B, C, D, rVec)

        self.handlePotentialAttackTarget(level.player, A, B, C, D, rVec)

        pyxel.play(1, 1)

    def teleport(self, x=0, y=0):
        if isinstance(x, Vector2):
            self.teleport(x.X, x.Y)
        else:
            self.location = Vector2(x, y)

    def step(self, step, level):
        newLoc = self.location + step
        # check if new loc is walkable
        if level.isWalkable(newLoc):
            self.location = newLoc
            return True
        else:
            return False

    def move(self, mX, mY, level):
        rVec = Vector2(mX, mY)
        if rVec.Y >= 0:
            self.lastForward = True
        else:
            self.lastForward = False

        steps = rVec.getLength()
        step = rVec / steps
        while(steps > 1):
            self.step(step, level)
            steps -= 1

        if (steps > 0):
            self.step(step * steps, level)

    def moveTowards(self, target, level):
        stepSpeed = self.movementSpeed
        dVec = target - self.location
        if dVec.getLength() == 0:
            return

        rVec = dVec.getNormalized() * stepSpeed
        self.move(rVec.X, rVec.Y, level)

    def update(self, level):
        if self.vX != 0 or self.vY != 0:
            self.move(self.vX, self.vY, level)
            self.vX = 0.9 * self.vX
            self.vY = 0.9 * self.vY
            if abs(self.vX) < 0.1:
                self.vX = 0
            if abs(self.vY) < 0.1:
                self.vY = 0

    def draw(self, camera):
        if self.lastAttackTime + 0.1 > time.time() and self.lastAttackLocation is not None:
            drawLoc = camera.getRelativeDrawPosition(self.lastAttackLocation)
            if drawLoc is not None:
                if self.lastAttackDirection == 0:
                    pyxel.blt(drawLoc.X - 16, drawLoc.Y - 32,
                              0, 0, 192, 32, 32, 3)
                elif self.lastAttackDirection == 4:
                    pyxel.blt(drawLoc.X - 16, drawLoc.Y,
                              0, 32, 192, 32, 32, 3)
                elif self.lastAttackDirection == 2:
                    pyxel.blt(drawLoc.X, drawLoc.Y - 16,
                              0, 0, 160, 32, 32, 3)
                elif self.lastAttackDirection == 6:
                    pyxel.blt(drawLoc.X - 32, drawLoc.Y - 16,
                              0, 32, 160, 32, 32, 3)
                elif self.lastAttackDirection == 1:
                    pyxel.blt(drawLoc.X - 8, drawLoc.Y - 32,
                              0, 64, 160, 32, 32, 3)
                elif self.lastAttackDirection == 7:
                    pyxel.blt(drawLoc.X - 24, drawLoc.Y - 35,
                              0, 96, 160, 32, 32, 3)
                elif self.lastAttackDirection == 5:
                    pyxel.blt(drawLoc.X - 24, drawLoc.Y, 0, 64, 192, 32, 32, 3)
                elif self.lastAttackDirection == 3:
                    pyxel.blt(drawLoc.X - 8, drawLoc.Y, 0, 96, 192, 32, 32, 3)
