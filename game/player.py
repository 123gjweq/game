from pyglet.window import key
import math

from vector2 import Vector2
from constants import *

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector2()

        self.health = 100
        self.max_health = 100

        self.sprites = [INJURED4SPRITE, INJURED3SPRITE, INJURED2SPRITE, INJURED1SPRITE, INJURED0SPRITE]
        self.image_selected_index = 4
        self.image_selected = self.sprites[self.image_selected_index]

        self.accel_constant = .5
        self.icyness = -.1
        self.accel = Vector2()

        self.player_camera = Vector2(750, 450)

    def Move(self, keys, dt):
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
        self.player_camera -= self.vel * dt

        self.accel.Clear()

    def Update(self, keys, dt, is_leftclicking, mouse_pos):
        self.Move(keys, dt * 60)

        # update image by players health
        self.image_selected_index = math.floor((self.health - 1) / (self.max_health / len(self.sprites)))
        self.image_selected = self.sprites[self.image_selected_index]
        #update le position relative to camera
        self.image_selected.x, self.image_selected.y = 750, 450