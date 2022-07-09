from reusableClasses.vector2 import Vector2
import pyglet

class Wall:

    color = (255, 255, 255)
    walls = []
    wallBatch = []

    def __init__(self, x, y, w, h):
        self.pos = Vector2(x, y)
        self.width = w
        self.height = h

        self.init_x, self.init_y = x, y
        #these are static variables that we dont change so we can optomize wall loading in

        rect = pyglet.shapes.Rectangle(self.pos.x, self.pos.y, self.width, self.height, Wall.color)
        Wall.walls.append(self)
        Wall.wallBatch.append(rect)