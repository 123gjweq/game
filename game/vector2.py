import math

class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, value):
        return Vector2(self.x * value, self.y * value)

    def __truediv__(self, value):
        return Vector2(self.x / value, self.y / value)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __round__(self):
        return Vector2(round(self.x), round(self.y))

    def GetNormalized(self):
        if self.length != 0:
            return Vector2(self.x / self.length, self.y / self.length)
        return Vector2(0, 0)

    def Clear(self):
        self.x = 0
        self.y = 0

    @property
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def angle(self):
        ang = math.atan2(-self.y, self.x)
        return ang + 2 * math.pi if ang < 0 else ang

    def tuple(self):
        return self.x, self.y