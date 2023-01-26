import Vector2
from Map.TilePresets.CorridorTile import CorridorTile
from Map.TilePresets.EmptyTile import EmptyTile
import Config
from Map.Room import Room
import MathUtils
import Map.Helper as Helper


class Corridor():
    def __init__(self, roomA: Room, roomB: Room, level, tileIndex=0):
        print(f"Corridor between {roomA.center} and {roomB.center}")
        # A corridor connects two rooms.
        self.roomA = roomA
        self.roomB = roomB
        self.tileIndex = tileIndex
        self.level = level
        # We calculate the tiles needed to connect the two rooms.
        #self.connectionPointA, self.connectionPointB = self.getConnectionPoints()

        self.tiles = []
        self.generateTiles()

    def getTiles(self):
        return self.tiles

    def generateTiles(self):
        self.tiles = []

        # We draw a line between the two connection points and add the tiles along the way, as well as points to the side of them (so the corridor is a bit bigger)
        coordSet = set()
        points = MathUtils.getConnectionPath(Helper.LocationToTile(
            self.roomA.center), Helper.LocationToTile(self.roomB.center))

        for point in points:
            for x in range(point.X-1, point.X+1):
                for y in range(point.Y-1, point.Y+1):
                    coordSet.add((x, y))

        for coord in coordSet:
            tX = int(coord[0])
            tY = int(coord[1])
            # currentTile = self.level.getTile(tX, tY)
            # if type(currentTile) is EmptyTile:
            self.tiles.append(CorridorTile(tX, tY, self.tileIndex))

    # def getConnectionPoints(self):
    #     # We send a ray from the center of the roomA to the center of the roomB, the two collisions are our two connection tiles.
    #     pointA = None
    #     pointB = None
    #     # We iterate over all 4 sides of room A and find the one our ray intersects with
    #     for side in range(4):
    #         A = self.roomA.getCorner(side)
    #         B = self.roomA.getCorner((side + 1) % 4)
    #         intersection = MathUtils.findIntersection(
    #             self.roomA.center, self.roomB.center, A, B)
    #         if intersection is not None:
    #             pointA = intersection
    #             break

    #     # We iterate over all 4 sides of room B and find the one our ray intersects with
    #     for side in range(4):
    #         A = self.roomB.getCorner(side)
    #         B = self.roomB.getCorner((side + 1) % 4)
    #         intersection = MathUtils.findIntersection(
    #             self.roomA.center, self.roomB.center, A, B)
    #         if intersection is not None:
    #             pointB = intersection
    #             break

    #     return pointA, pointB
