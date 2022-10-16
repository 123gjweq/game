import time

from constants import *
from reusableClasses.collisions import Collision

class Gun:

    walls = []
    upgrades = \
    [ # in the form: damage, bullet_speed, time_between_bullets, reload_time, automatic
    #sound is determined by the automatic or not.
        [10, 20, 0.3, 1, False],
        [10, 20, 0.2, 1, True],
        [15, 20, 0.2, 1, True],
        [20, 20, 0.2, 1, True],
        [20, 30, 0.15, 1, True],
        [20, 30, 0.125, 0.5, True],
        [20, 35, 0.125, 0.5, True],
        [100, 10, 2, 1, False],
        [25, 30, 0.125, 1, True],
        [25, 30, 0.125, 0.5, True]
    ]

    def __init__(self, pos):
        self.bullets = []

        self.pos = pos
        
        # upgrades
        self.damage = Gun.upgrades[0][0]
        self.bullet_speed = Gun.upgrades[0][1]
        self.time_between_bullets = Gun.upgrades[0][2]
        self.reload_time = Gun.upgrades[0][3]
        self.automatic = Gun.upgrades[0][4]

        self.able_to_shoot = True

        self.distance_bullet_can_travel = 800
        self.time_last_shot = 0

        self.semi_automatic_check_if_shoot = True

        self.clip_size = 20
        self.bullets_left = 20
        self.time_started_reloading = 0

    def ChangeStats(self, stats):
        self.damage = stats[0]
        self.bullet_speed = stats[1]
        self.time_between_bullets = stats[2]
        self.reload_time = stats[3]
        self.automatic = stats[4]

    def Update(self, pos, mouse_pos, is_leftclicking, dt):
        self.pos = pos
        shot = False #temp var (stands for temporary variable)
        
        # check if you should shoot
        # automatic check
        if (time.time() - self.time_last_shot) > self.time_between_bullets and self.bullets_left > 0 and self.able_to_shoot:
            if is_leftclicking and self.automatic:
                self.Shoot(mouse_pos)
                shot = True
            #semiautomatic check
            if is_leftclicking and self.semi_automatic_check_if_shoot:
                self.Shoot(mouse_pos)
                self.semi_automatic_check_if_shoot = False
                shot = True
            elif is_leftclicking is False:
                self.semi_automatic_check_if_shoot = True

        if time.time() > self.time_started_reloading + self.reload_time and self.time_started_reloading != 0:
            self.able_to_shoot = True
            self.bullets_left = self.clip_size
            self.time_started_reloading = 0
        if shot:
            return (self.automatic, self.pos)


    def Shoot(self, mouse_pos):
        # pos is relative to screen
        direction_of_bullet = (mouse_pos - Vector2(SCREENWIDTH / 2, SCREENHEIGHT / 2)).GetNormalized()
        # check if bullet hits wall
        contact_point = Vector2()
        lowestLengthOfWall = Bullet.distance_can_travel
        for wall in Gun.walls:
            if Collision.RectOnRay(self.pos, direction_of_bullet, wall.pos, wall.width, wall.height, contact_point):
                lengthOfWall = (contact_point - self.pos).length
                if lengthOfWall < lowestLengthOfWall:
                    lowestLengthOfWall = lengthOfWall

        self.bullets.append(Bullet(self.pos, direction_of_bullet, self.bullet_speed, lowestLengthOfWall))
        self.bullets_left -= 1
        self.time_last_shot = time.time()

    def Reload(self):
        self.time_started_reloading = time.time()
        self.able_to_shoot = False


class Bullet:

    distance_can_travel = 700

    def __init__(self, pos, dir, speed, distance_to_travel):
        self.pos = pos
        self.dir = dir.GetNormalized()
        self.distance_to_travel = distance_to_travel
        self.distance_traveled = 0
        self.speed = speed
        self.time_shot = time.time()

    @property
    def should_die(self):
        if self.distance_traveled > self.distance_to_travel:
            return True
        return False

    def Move(self, dt):
        movement = (self.dir * self.speed) * dt
        self.pos += movement
        self.distance_traveled += movement.length