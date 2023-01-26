import collections
from enum import Enum
import heapq
from time import perf_counter


class PathfinderNodeFlag(Enum):
    NONE = 1,
    OPEN = 2,
    CLOSED = 4,


class PathfinderNode:
    def __init__(self):
        self.pf_reset()

    def pf_reset(self):
        self.g = 0
        self.h = -1
        self.flag = PathfinderNodeFlag.NONE
        self.parent = None

    def __lt__(self, other):
        return self.g + self.h < other.g + other.h

    def getHeuristic(self, other):
        # To be implemented by the derrived class
        print("ERROR: PathfinderNode.getHeuristic() not implemented")
        pass

    def getMovementCost(self, other):
        # To be implemented by the derrived class, if other than 1 is wanted
        return 1


class PathfinderQueue:
    # A simple wrapper around qheap, because I don't like typing so much
    def __init__(self):
        self.clear()

    def empty(self):
        return not self.elements or len(self.elements) == 0

    def push(self, v):
        heapq.heappush(self.elements, (v.g + v.h, v))

    def pop(self):
        return heapq.heappop(self.elements)[1]

    def update(self, neighbor):
        heapq.heapify(self.elements)

    def clear(self):
        self.elements = []


class Pathfinder:
    # A simple A* pathfinder
    def __init__(self):
        self.openList = PathfinderQueue()
        self.modifiedList = []

    def reset(self):
        self.openList.clear()
        for node in self.modifiedList:
            node.pf_reset()

        self.modifiedList = []

    def reconstructPath(self, node: PathfinderNode):
        path = []
        while (node.parent != None):
            path.append(node)
            node = node.parent

        path.reverse()
        
        return path

    def updateOpenNode(self, node):
        # self.openList.update(node)
        pass

    def openNode(self, node):
        node.flag = PathfinderNodeFlag.OPEN
        self.openList.push(node)
        self.modifiedList.append(node)

    def checkNeighbors(self, current, start, end, level):
        neighbors = level.getNeighbors(current)
        for neighbor in neighbors:
            newCost = current.g + current.getMovementCost(neighbor)

            if (neighbor.flag == PathfinderNodeFlag.NONE or newCost < neighbor.g) and neighbor != start:
                neighbor.g = newCost
                neighbor.parent = current
                if neighbor.h == -1:
                    neighbor.h = neighbor.getHeuristic(end)

            if neighbor.flag == PathfinderNodeFlag.OPEN:
                # Already in open list
                self.updateOpenNode(neighbor)
            else:
                self.openNode(neighbor)

    def findPath(self, start: PathfinderNode, end: PathfinderNode, level: object):
        startTime = perf_counter()
        self.reset()
        self.openList.push(start)

        if start == end:
            return [start]

        iterations = 0
        # A* :)
        while(not self.openList.empty()):
            current = self.openList.pop()
            iterations += 1
            if (current == end):
                path = self.reconstructPath(current)
                #print(f"Processed {iterations} nodes for a path of length {len(path)} in {perf_counter() - startTime} ms")
                return path

            current.flag == PathfinderNodeFlag.CLOSED
            self.checkNeighbors(current, start, end, level)

        # No path
        #print(f"Processed {iterations} nodes for NO path in {perf_counter() - startTime} ms")
        return []
