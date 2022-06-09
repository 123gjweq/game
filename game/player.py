from pyglet.window import key
import math

from vector2 import Vector2
from constants import *

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector2(0, 0)

        self.health = 100
        self.maxHealth = 100

        self.images = [INJURED0, INJURED1, INJURED2, INJURED3, INJURED4]
        self.imageSelectedIndex = 0
        self.imageSelected = self.images[self.imageSelectedIndex]

        self.accel_constant = .5
        self.icyness = -.1
        self.accel = Vector2(0, 0)

    def Move(self, keys, dt):
        # Update Velocity
        if keys[key.W]:
            self.accel.y = self.accel_constant
        if keys[key.S]:
            self.accel.y = -self.accel_constant
        if keys[key.A]:
            self.accel.x = -self.accel_constant
        if keys[key.D]:
            self.accel.x = self.accel_constant

        if self.accel.x != 0 and self.accel.y != 0:
            self.accel.x, self.accel.y = self.accel.x * .707, self.accel.y * .707 #.707 is approximately the reciprocal of sqrt 2.

        self.accel.x += self.vel.x * self.icyness
        self.accel.y += self.vel.y * self.icyness

        #movement
        self.vel += self.accel * dt
        # x side
        self.pos.x += self.vel.x * dt
        # y side
        self.pos.y += self.vel.y * dt

        self.accel.x, self.accel.y = 0, 0

    def Update(self, keys, leftClicking, dt):
        self.Move(keys, dt * 60)

        # update image by players health
        if self.health == self.maxHealth:
            self.imageSelectedIndex = len(self.images) - 1
        else:
            self.imageSelectedIndex = math.floor(self.health / (self.maxHealth / len(self.images)))
        self.imageSelected = self.images[self.imageSelectedIndex]