from pyglet.window import key
import math
from reusableClasses.vector2 import Vector2
from constants import *
class Player:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector2()
        self.health = 100
        self.max_health = 100
        self.accel_constant = .5
        self.icyness = -.1
        self.accel = Vector2()
        self.image_index = math.floor((self.health - 1) / (self.max_health / 5))
        self.camera = Vector2(750, 450)

    def Move(self, keys, dt):
        """
        # Update Velocity
        if keys[key.W]:
            self.accel.y += self.accel_constant
        if keys[key.S]:
            self.accel.y += -self.accel_constant
        if keys[key.A]:
            self.accel.x += -self.accel_constant
        if keys[key.D]:
            self.accel.x += self.accel_constant
        if self.accel.x != 0 and self.accel.y != 0:
            self.accel.x, self.accel.y = self.accel.x * .707, self.accel.y * .707 #.707 is approximately the reciprocal of sqrt 2.
        #movement
        self.accel += (self.vel * self.icyness) * dt
        self.vel += self.accel * dt
        self.pos += self.vel * dt
        #move camera
        self.camera -= self.vel * dt
        self.accel.Clear()
        """
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


    def Update(self, keys, dt, is_leftclicking, mouse_pos):
        self.Move(keys, dt * 60)
        # update index by players health
        self.image_index = math.floor((self.health - 1) / (self.max_health / 5))