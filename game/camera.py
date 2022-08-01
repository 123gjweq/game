from reusableClasses.vector2 import Vector2

class Camera:
    def __init__(self, pos):
        self.pos = pos

    @property
    def offset(self):
        return self.pos * -1
