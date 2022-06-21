from pyglet.window import key
import math

from reusableClasses.vector2 import Vector2
from constants import *
from gun import Gun

class Player:
    def __init__(self, pos):
        self.pos = Vector2(pos[0], pos[1])
        self.poses = [self.pos] * 10
        self.num_of_pos_frames = 50
        self.vel = Vector2()

        self.health = 100
        self.max_health = 100

        self.angle_looking = 0

        self.image_index = math.floor((self.health - 1) / (self.max_health / 5))

        self.camera = Vector2(750, 450)

        self.gun = Gun(self.pos)

    def calculate_next_pos(self, dt):
        for x in range(self.num_of_pos_frames):
            self.poses.append(self.pos + (self.vel * (x * dt)))

    def Move(self, keys, dt):
        if int(TIMEBETWEENSEND * dt * 60) + 1 > self.num_of_pos_frames:
            self.pos = self.poses[-1]
        else:
            self.pos = self.poses[int(TIMEBETWEENSEND * dt * 60)]

        self.poses.clear()

        self.vel.x = NO.x
        self.vel.y = NO.y
        if keys[key.W]:
            self.vel.y = VEL_CONST
        if keys[key.S]:
            self.vel.y = -VEL_CONST
        if keys[key.A]:
            self.vel.x = -VEL_CONST
        if keys[key.D]:
            self.vel.x = VEL_CONST

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel = self.vel * .707 #.707 is approximately the reciprocal of sqrt 2.

        self.pos += self.vel * dt
        self.calculate_next_pos(dt)
        

    def Update(self, keys, dt, mouse_pos, is_leftclicking):
        self.Move(keys, dt * 60)
        
        self.angle_looking = math.degrees((mouse_pos - Vector2(SCREENWIDTH / 2, SCREENHEIGHT / 2)).angle) + 90 # use screen dim cuz player centered
        self.gun.Update(self.pos, mouse_pos, is_leftclicking, dt * 60)

        # update index by players health
        self.image_index = math.floor((self.health - 1) / (self.max_health / 5))