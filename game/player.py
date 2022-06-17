from pyglet.window import key
import math

from reusableClasses.vector2 import Vector2
from constants import *
from gun import Gun

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector2()

        self.health = 100
        self.max_health = 100

        self.angle_looking = 0

        self.image_index = math.floor((self.health - 1) / (self.max_health / 5))

        self.camera = Vector2(750, 450)

        self.gun = Gun(self.pos)

    def Move(self, keys, dt):
        self.vel.x = NO.x
        self.vel.y = NO.y
        if keys[key.W]:
            self.vel.y = 5
        if keys[key.S]:
            self.vel.y = -5
        if keys[key.A]:
            self.vel.x = -5
        if keys[key.D]:
            self.vel.x = 5

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel = self.vel * .707 #.707 is approximately the reciprocal of sqrt 2.

        self.pos += self.vel * dt
        self.camera -= self.vel * dt
        

    def Update(self, keys, dt, mouse_pos, is_leftclicking):
        self.Move(keys, dt * 60)
        
        self.angle_looking = math.degrees((mouse_pos - Vector2(SCREENWIDTH / 2, SCREENHEIGHT / 2)).angle) + 90 # use screen dim cuz player centered
        self.gun.Update(self.pos, mouse_pos, is_leftclicking, dt * 60)

        # update index by players health
        self.image_index = math.floor((self.health - 1) / (self.max_health / 5))