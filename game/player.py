from pyglet.window import key
import math
import time

from gun import Gun
from wall import Wall
from camera import Camera
from constants import *

from reusableClasses.vector2 import Vector2
from reusableClasses.collisions import Collision

class Player:

    walls = []

    def __init__(self, pos):
        self.pos = pos
        self.vel = Vector2()

        self.health = 100
        self.max_health = 100

        self.angle_looking = 0
        self.last_two_angles = [0, 0]

        self.camera = Camera(Vector2(0, 0))
        self.gun = Gun(self.pos)

        self.kills = 0

        self.time_last_hit = 0
        self.time_last_healed = 0

        self.username = ''

        self.sound_info = None

    def Move(self, keys, dt):
        self.vel.Clear()

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
        
        # move and update camera
        self.pos += self.vel * dt

        #check if there are any collisions with the walls
        for wall in Wall.walls:
            colliding, pos = Collision.CircleOnRect(self.pos, 25, wall.pos, wall.width, wall.height)
            if colliding:
                self.pos = pos
        
        self.camera.pos = self.pos - Vector2(SCREENWIDTH/2, SCREENHEIGHT/2)


    def Update(self, client_data):
        self.dt = client_data.dt
        self.Move(client_data.keys, self.dt * 60)
        self.angle_looking = client_data.angle_looking
        self.last_two_angles = client_data.last_two_angles

        self.sound_info = self.gun.Update(self.pos, client_data.mouse_pos, client_data.left_clicking, self.dt * 60)

        if time.time() > self.time_last_hit + 5 and time.time() > self.time_last_healed + 1:
            self.health += 2
            self.time_last_healed = time.time()
            
        if client_data.keys[key.R] and self.gun.able_to_shoot:
            self.gun.Reload()


    @property
    def image_index(self):
        return math.floor((self.health - 1) / (self.max_health / 5))