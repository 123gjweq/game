import time
from random import randrange

from constants import *

class Gun:

    def __init__(self, pos):
        self.bullets = []

        self.pos = pos
        
        self.damage = 10
        self.bullet_speed = 20
        self.time_between_bullets = 0.3 # in seconds
        self.reload_time = 1 # in seconds
        self.automatic = True
        self.distance_bullet_can_travel = 800

        self.time_last_shot = 0

        self.semi_automatic_check_if_shoot = True

    def Update(self, pos, mouse_pos, is_leftclicking, dt):
        self.pos = pos
        
        # check if you should shoot
        # automatic check
        if is_leftclicking and self.automatic:
            self.Shoot(mouse_pos)
        #semiautomatic check
        if is_leftclicking and self.semi_automatic_check_if_shoot:
            self.Shoot(mouse_pos)
            self.semi_automatic_check_if_shoot = False
        elif is_leftclicking is False:
            self.semi_automatic_check_if_shoot = True

    def Shoot(self, mouse_pos):
        if (time.time() - self.time_last_shot) > self.time_between_bullets:
            # pos is relative to screen
            direction_of_bullet = (mouse_pos - Vector2(SCREENWIDTH / 2, SCREENHEIGHT / 2))
            self.bullets.append(Bullet(self.pos, direction_of_bullet, self.bullet_speed))
            self.time_last_shot = time.time()


class Bullet:

    def __init__(self, pos, dir, speed):
        self.pos = pos
        self.dir = dir.GetNormalized()
        self.distance_can_travel = 0
        self.speed = speed
        self.time_shot = time.time()
        self.ID = randrange(5000)


    def Move(self, dt):
        movement = (self.dir * self.speed) * dt
        self.pos += movement
        self.distance_can_travel += movement.length