from this import d
import Config
from Vector2 import Vector2
from Map.Corridor import Corridor
from Map.TilePresets.EmptyTile import EmptyTile
from Map.TilePresets.WallTile import WallTile
from Camera import Camera
from Map.Room import Room
from Map.Rooms.StandardRoom import StandardRoom
from Map.Pathfinder import Pathfinder
from Actor.Player import Player
from Actor.Monster import Monster
from Map.Stair import Stair

import Map.Helper as Helper
import MathUtils
import math
import random
import pyxel


class Level:
    def __init__(self, levelNumber, player: Player):
        self.levelNumber = levelNumber
        self.player = player
        self.load()

    def load(self):
        # We load the level.
        levelSize = (Config.BASE_LEVEL_PIXEL_SIZE +
                     ((Config.BASE_LEVEL_PIXEL_SIZE / 20) * self.levelNumber))
        # Making sure it is a multiple of TILE_PIXEL_SIZE
        levelSize = int((levelSize // Config.TILE_PIXEL_SIZE)
                        * Config.TILE_PIXEL_SIZE)

        self.roomCount = 1
        self.rooms = []
        self.corridors = []
        self.tiles = []
        self.enemies = []
        self.tileWidth = int(levelSize / Config.TILE_PIXEL_SIZE) + 1
        self.tileHeight = self.tileWidth
        self.camera = Camera(self)
        self.pathfinder = Pathfinder()
        self.stair = Stair()
        self.initEmpty()
        self.generateLevel()
        self.player.hp = self.player.maxHP

    def getTile(self, tX, tY):
        return self.tiles[tX][tY]

    def initEmpty(self):
        self.tiles = []
        # Set tiles table to empty tiles
        for tX in range(self.tileWidth):
            self.tiles.append([])
            for tY in range(self.tileHeight):
                # Default empty Tile
                self.tiles[tX].append(EmptyTile(tX, tY))

    def calculateRoomCount(self):
        # We want on average to have one room per 10000 tiles
        tmp = math.ceil(self.tileWidth * self.tileHeight / 3000)
        # Adding some random variation (0.5 - 1.5)
        mlt = random.random() + 0.5

        self.roomCount = max(int(tmp * mlt), 1)
        return self.roomCount

    def generateRoom(self) -> Room:
        # We select a random location
        roomTileWidth = random.randint(
            min(12, self.tileWidth), min(40, self.tileWidth))
        # print(roomTileWidth)
        roomTileHeight = random.randint(
            min(12, self.tileHeight), min(40, self.tileHeight))
        # print(roomTileHeight)
        # print(self.tileWidth, self.tileHeight)
        tX = random.randint(int(roomTileWidth / 2) + 1,
                            self.tileWidth - int(roomTileWidth / 2) - 1)
        tY = random.randint(int(roomTileHeight / 2) + 1,
                            self.tileHeight - int(roomTileHeight / 2) - 1)

        newRoom = StandardRoom(Vector2(tX, tY), roomTileWidth, roomTileHeight)
        return newRoom

    def generateCorridor(self, roomA, roomB):
        # We check if we can already move from roomA to roomB in reasonable distance
        roomATile = self.getTile(roomA.centerTilePos.X, roomA.centerTilePos.Y)
        roomBTile = self.getTile(roomB.centerTilePos.X, roomB.centerTilePos.Y)

        path = self.pathfinder.findPath(roomATile, roomBTile, self)
        maxAllowedPathLength = roomA.centerTilePos.getDistance(
            roomB.centerTilePos) * 4
        pathLen = len(path)
        if (pathLen > 0 and pathLen < maxAllowedPathLength):
            return

        newCorridor = Corridor(roomA, roomB, self, len(self.corridors) % 4)
        if (len(newCorridor.getTiles()) > 0):
            self.corridors.append(newCorridor)
            tiles = newCorridor.getTiles()
            for tile in tiles:
                if tile.tX < len(self.tiles):
                    if tile.tY < len(self.tiles[tile.tX]):
                        self.tiles[tile.tX][tile.tY] = tile

    def generateMonster(self, room):
        minX = int(room.centerTilePos.X - room.tileWidth / 2) + 2
        maxX = int(room.centerTilePos.X + room.tileWidth / 2) - 2
        minY = int(room.centerTilePos.Y - room.tileHeight / 2) + 2
        maxY = int(room.centerTilePos.Y + room.tileHeight / 2) - 2
        monsterX = random.randint(minX, maxX)
        monsterY = random.randint(minY, maxY)
        newMonster = Monster(self.levelNumber)

        mLoc = Helper.TileToLocation(Vector2(monsterX, monsterY))
        newMonster.teleport(mLoc.X, mLoc.Y)
        return newMonster

    def generateLevel(self):
        roomCount = self.calculateRoomCount()
        # We generate the rooms.
        self.rooms = []
        for i in range(roomCount):
            self.rooms.append(self.generateRoom())

        # We load all the rooms
        for room in self.rooms:
            room.load()
            newTiles = room.getTiles()
            for tile in newTiles:
                if not (self.tiles[tile.tX][tile.tY].walkable and not tile.walkable):
                    self.tiles[tile.tX][tile.tY] = tile

        if len(self.rooms) > 1:
            # We generate the corridors.
            self.corridors = []
            for i in range(len(self.rooms)):
                roomA = self.rooms[i]
                for j in range(i + 1, len(self.rooms)):
                    roomB = self.rooms[j]
                    self.generateCorridor(roomA, roomB)

        # We teleport the player to the start room
        startRoom = self.rooms[0]
        endRoom = self.rooms[len(self.rooms) - 1]
        self.player.teleport(startRoom.center.X, startRoom.center.Y)

        # We generate the wall tiles
        for tX in range(self.tileWidth):
            for tY in range(self.tileHeight):
                if not self.tiles[tX][tY].walkable:
                    # If the tile to the right or bottom is walkable, it is a wall
                    if (tX < self.tileWidth - 1 and self.tiles[tX + 1][tY].walkable):
                        self.tiles[tX][tY] = WallTile(tX, tY)
                    elif (tY < self.tileHeight - 1 and self.tiles[tX][tY + 1].walkable):
                        self.tiles[tX][tY] = WallTile(tX, tY)
                    # If the bottom right is walkable, but the right and bottom is not, it is also a wall
                    elif (tX < self.tileWidth - 1 and tY < self.tileHeight - 1 and self.tiles[tX + 1][tY + 1].walkable and not self.tiles[tX][tY + 1].walkable and not self.tiles[tX+1][tY].walkable):
                        self.tiles[tX][tY] = WallTile(tX, tY)
                    # # If the top right is walkable, but the right and top and bottom is not, it is also a wall
                    # elif (tX < self.tileWidth - 1 and tY > 0 and self.tiles[tX + 1][tY - 1].walkable and not self.tiles[tX][tY + 1].walkable and not self.tiles[tX][tY - 1].walkable and not self.tiles[tX+1][tY].walkable):
                    #     self.tiles[tX][tY] = WallTile(tX, tY)

        # We generate the enemies
        for room in self.rooms:
            monsterCount = random.randint(7, int(15 * 1+(self.levelNumber/5)))
            for i in range(monsterCount):
                newMonster = self.generateMonster(room)
                if newMonster.location.getDistance(self.player.location) > 80:
                    self.enemies.append(newMonster)

        # We place the stairs on a random tile in a random room
        stairsRoom = random.choice(self.rooms)
        tile = random.choice(stairsRoom.getTiles())
        self.stair.location = Helper.TileToLocation(
            tile.tilePos) + Vector2(8, 8)

    directions = [Vector2(0, -1), Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0)]

    def getNeighbors(self, tile):
        # Checking in the 4 direct directions
        for direction in self.directions:
            neighbor = self.getTile(tile.tX + direction.X,
                                    tile.tY + direction.Y)
            if neighbor.walkable:
                yield neighbor

        # Checking in the 4 diagonal directions
        topLeft = self.getTile(tile.tX - 1, tile.tY - 1)
        top = self.getTile(tile.tX, tile.tY - 1)
        topRight = self.getTile(tile.tX + 1, tile.tY - 1)
        left = self.getTile(tile.tX - 1, tile.tY)
        right = self.getTile(tile.tX + 1, tile.tY)
        bottomLeft = self.getTile(tile.tX - 1, tile.tY + 1)
        bottom = self.getTile(tile.tX, tile.tY + 1)
        bottomRight = self.getTile(tile.tX + 1, tile.tY + 1)
        if topLeft.walkable and left.walkable and top.walkable:
            yield topLeft

        if topRight.walkable and top.walkable and right.walkable:
            yield topRight

        if bottomLeft.walkable and left.walkable and bottom.walkable:
            yield bottomLeft

        if bottomRight.walkable and bottom.walkable and right.walkable:
            yield bottomRight

    def update(self, app):
        self.player.update(self)
        self.camera.update(self.player)
        for enemy in self.enemies:
            if enemy.hp <= 0:
                pyxel.play(1, 2)
                self.enemies.remove(enemy)
                app.gold += math.floor(5 * (self.levelNumber *
                                            (0.3 + random.random() * 2.7)))

            enemy.update(self)

        if self.stair.location.getDistance(self.player.location) < 8:
            pyxel.play(1, 3)
            return 1

        if self.player.hp <= 0:
            pyxel.play(1, 4)
            return 2

        return 0

    def isWalkable(self, location):
        tileLoc = Helper.LocationToTile(location)
        if tileLoc.X < 0 or tileLoc.X >= self.tileWidth or tileLoc.Y < 0 or tileLoc.Y >= self.tileHeight:
            return False

        tile = self.getTile(tileLoc.X, tileLoc.Y)
        if tile.walkable:
            return True

        return False

    def draw(self):
        # Draw tiles
        for tiles in self.tiles:
            for tile in tiles:
                # print(tile)
                tile.draw(self.camera, self)

        # Drawing the player
        self.player.draw(self.camera)

        for enemy in self.enemies:
            enemy.draw(self.camera)

        self.stair.draw(self.camera)

        # Draw debug info
        # pyxel.text(0, 0, "Level: " + str(self.levelNumber), 3)
        # pyxel.text(0, 10, "Player Location: " + str(self.player.location), 3)
        # pyxel.text(0, 20, "Player Tile Location: " +
        #            str(Helper.LocationToTile(self.player.location)), 3)
        # mouseLoc = Helper.GetMouseLocation(self.camera)
        # pyxel.text(0, 30, f"Mouse Location: {mouseLoc}", 3)
        # pyxel.text(0, 40, "Room Count: " + str(self.roomCount), 3)
        # pyxel.text(0, 50, "Corridor Count: " + str(len(self.corridors)), 3)
        # y = 60
        # for room in self.rooms:
        #     pyxel.text(
        #         0, y, f"Room at {room.center} with tile size {room.tileWidth}, {room.tileHeight}", 3)
        #     y += 10

        # for corridor in self.corridors:
        #     A = self.camera.getRelativeDrawPosition(
        #         corridor.roomA.center, True)
        #     B = self.camera.getRelativeDrawPosition(
        #         corridor.roomB.center, True)

        #     pyxel.line(A.X, A.Y, B.X, B.Y, 3)
