from importlib.resources import path
from Actor.Actor import Actor
import Map.Helper as Helper
from Vector2 import Vector2
import ResourceHelper
import pyxel
import random


class Monster(Actor):
    def __init__(self, levelNumber):
        super().__init__()
        self.path = []
        self.currentWaypoint = None
        self.lastDst = Vector2(0, 0)
        mult = (1 + levelNumber / 4)
        self.movementSpeed = 0.5 * (1 + random.random() * mult)
        self.maxHP = 50 * (1 + random.random() * mult)
        self.hp = self.maxHP
        self.attackSpeed = 1 + random.random() * mult
        self.attackDamage = 4 * (1 + random.random() * mult)

    def recalculatePath(self, level):
        startTileLoc = Helper.LocationToTile(self.location)
        endTileLoc = Helper.LocationToTile(self.lastDst)
        startTile = level.getTile(startTileLoc.X, startTileLoc.Y)
        endTile = level.getTile(endTileLoc.X, endTileLoc.Y)
        self.path = level.pathfinder.findPath(startTile, endTile, level)
        self.currentWaypoint = None

    def pathToNextWaypoint(self, level):
        if self.currentWaypoint is None or self.currentWaypoint.getDistance(self.location) < 3:
            if len(self.path) == 0:
                # we reached
                self.path = []
                self.currentWaypoint = None
                self.lastDst = self.location
            else:
                tileWaypoint = self.path.pop(0)
                self.currentWaypoint = Helper.TileToLocation(
                    tileWaypoint.tilePos)

        if self.currentWaypoint is not None:
            self.moveTowards(self.currentWaypoint, level)

    def pathTo(self, dst, level):
        dstToLast = self.lastDst.getDistance(dst)
        if dstToLast > 64 or dst.getDistance(self.location) < 64:
            self.lastDst = dst
            self.recalculatePath(level)

        self.pathToNextWaypoint(level)

    def update(self, level):
        # Check distance to player
        pLoc = level.player.location
        distance = self.location.getDistance(pLoc)
        if distance < 128 or (len(self.path) > 0 and distance < 256):
            self.pathTo(pLoc, level)

        if distance < 12:
            self.attack(pLoc - self.location, level)

        super().update(level)

    def isEnemy(self, other):
        return type(other) is not Monster

    def draw(self, camera):
        location = Vector2(self.location)
        location.X -= 8
        location.Y -= 8
        drawLoc = camera.getRelativeDrawPosition(location)
        if drawLoc is not None:
            ResourceHelper.DrawMonster(drawLoc, self.lastForward)
            if self.hp < self.maxHP:
                pyxel.rect(drawLoc.X, drawLoc.Y - 8,
                           16, 4, pyxel.COLOR_BLACK)
                pyxel.rect(drawLoc.X, drawLoc.Y - 8, 16 *
                           (self.hp / self.maxHP), 4, pyxel.COLOR_RED)

            super().draw(camera)

            # prevDrawLoc = drawLoc
            # for waypoint in self.path:
            #     loc = Helper.TileToLocation(waypoint.tilePos)
            #     nextDrawLoc = camera.getRelativeDrawPosition(loc)
            #     if nextDrawLoc is not None:
            #         pyxel.line(prevDrawLoc.X, prevDrawLoc.Y,
            #                    nextDrawLoc.X, nextDrawLoc.Y, 7)
            #         prevDrawLoc = nextDrawLoc
            #     else:
            #         break
