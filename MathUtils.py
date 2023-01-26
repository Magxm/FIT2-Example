# from __future__ import division
from Vector2 import Vector2
import math

# def findIntersection(A, B, C, D):
#     # Math taken from
#     # https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
#     # However check to see if intersection is on line segment was added and it was adapted to Vector2 class
#     x1 = A.X
#     y1 = A.Y
#     x2 = B.X
#     y2 = B.Y
#     x3 = C.X
#     y3 = C.Y
#     x4 = D.X
#     y4 = D.Y

#     denom = ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
#     if (denom == 0):
#         return None

#     px = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)) / denom

#     denom = ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
#     if (denom == 0):
#         return None

#     py = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)) / denom

#     # Check if the intersection is on the line segment
#     intersection = Vector2(px, py)
#     if (intersection.getDistance(A) + intersection.getDistance(B)) > A.getDistance(B):
#         return None

#     return intersection


def getConnectionPath(p1, p2):
    points = []
    x = p1.X
    y = p1.Y
    while(x != p2.X and y != p2.Y):
        points.append(Vector2(x, y))
        dx = p2.X - x
        dy = p2.Y - y
        if abs(dx) > abs(dy):
            x += 1 if dx > 0 else -1
        else:
            y += 1 if dy > 0 else -1

    points.append(Vector2(x, y))
    return points


def dist(p1, p2, c):
    x1, y1 = p1.X, p1.Y
    x2, y2 = p2.X, p2.Y
    x3, y3 = c.X, c.Y
    px = x2-x1
    py = y2-y1

    something = px*px + py*py

    u = ((x3 - x1) * px + (y3 - y1) * py) / float(something)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    dist = math.sqrt(dx*dx + dy*dy)

    return dist


def pointInRec(r, m):
    A = r[0]
    B = r[1]
    C = r[2]
    D = r[3]

    AB = B - A
    AM = m - A
    BC = C - B
    BM = m - B
    dotABAM = AB.dot(AM)
    dotABAB = AB.dot(AB)
    dotBCBM = BC.dot(BM)
    dotBCBC = BC.dot(BC)
    return 0 <= dotABAM and dotABAM <= dotABAB and 0 <= dotBCBM and dotBCBM <= dotBCBC


def hasCircleRectCollision(cLoc, cRadius, rect):
    distances = [dist(rect[i], rect[j], cLoc)
                 for i, j in zip([0, 1, 2, 3], [1, 2, 3, 0])]
    inside = any(d < cRadius for d in distances)
    if inside:
        return True

    return pointInRec(rect, cLoc)
