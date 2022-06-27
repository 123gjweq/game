from pyglet.window import key
import math
from reusableClasses.vector2 import Vector2
from constants import *
class Player:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector2()
        #the velocity
        self.lvel = Vector2()
        self.health = 100
        self.max_health = 100

        self.vel_constant = 5
        self.icyness = -.1
        self.accel = Vector2()

        self.image_index = math.floor((self.health - 1) / (self.max_health / 5))

        self.camera = Vector2(750, 450)

    def Move(self, keys, dt):
        # Update Velocity
        if keys[key.W]:
            self.vel.y += self.vel_constant
        if keys[key.S]:
            self.vel.y += -self.vel_constant
        if keys[key.A]:
            self.vel.x += -self.vel_constant
        if keys[key.D]:
            self.vel.x += self.vel_constant
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel = self.vel * .707 #.707 is approximately the reciprocal of sqrt 2.
        #movement
    
        self.pos += self.vel * dt
        #move camera
        self.camera -= self.vel * dt
        self.lvel.x, self.lvel.y = self.vel.x, self.vel.y
        self.vel.Clear()

    def Update(self, keys, dt, is_leftclicking, mouse_pos):
        self.Move(keys, dt * 60)

        # update index by players health
        self.image_index = math.floor((self.health - 1) / (self.max_health / 5)) 