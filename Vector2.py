import math


class Vector2:
    def __init__(self, x=0, y=0):
        self.X = x
        self.Y = y

        # Check if called as copy constructor
        if isinstance(x, Vector2):
            self.Y = x.Y
            self.X = x.X

    def __str__(self):
        return f"({self.X}, {self.Y})"

    def __add__(self, other):
        return Vector2(self.X + other.X, self.Y + other.Y)

    def __sub__(self, other):
        return Vector2(self.X - other.X, self.Y - other.Y)

    def __mul__(self, other):
        return Vector2(self.X * other, self.Y * other)

    def __truediv__(self, other):
        return Vector2(self.X / other, self.Y / other)

    def __floordiv__(self, other):
        return Vector2(self.X // other, self.Y // other)

    def __mod__(self, other):
        return Vector2(self.X % other, self.Y % other)

    def __pow__(self, other):
        return Vector2(self.X ** other, self.Y ** other)

    def __neg__(self):
        return Vector2(-self.X, -self.Y)

    def __pos__(self):
        return Vector2(+self.X, +self.Y)

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.X < other.X and self.Y < other.Y

    def __le__(self, other):
        return self.X <= other.X and self.Y <= other.Y

    def __gt__(self, other):
        return self.X > other.X and self.Y > other.Y

    def __ge__(self, other):
        return self.X >= other.X and self.Y >= other.Y

    def __hash__(self):
        return hash((self.X, self.Y))

    def __getitem__(self, key):
        return self.X if key == 0 else self.Y

    def __setitem__(self, key, value):
        if key == 0:
            self.X = value
        else:
            self.Y = value

    def __len__(self):
        return math.sqrt(self.X * self.X + self.Y * self.Y)

    def getLength(self):
        return self.__len__()

    def getDistance(self, other):
        return (other - self).getLength()

    def getNormalized(self):
        return self / self.getLength()

    def dot(self, other):
        return self.X * other.X + self.Y * other.Y
