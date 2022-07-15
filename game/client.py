import pyglet
from pyglet.window import key
from threading import Thread
from random import randrange
import time

from player import Player
from network import Network
from wall import Wall
from sentStuff import *
from constants import *

from reusableClasses.vector2 import Vector2
from reusableClasses.collisions import Collision


class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        #pygame stuff
        super().__init__(*args, **kwargs)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        self.frame_rate = 1/120.0
        self.mouse_pos = Vector2()
        self.left_clicking = False
        self.PLAYERSPRITES = [INJURED4SPRITE, INJURED3SPRITE, INJURED2SPRITE, INJURED1SPRITE, INJURED0SPRITE]

        # connection
        self.n = Network()
        # get ID
        self.ID = self.n.GetID("ID")
        # get map
        self.map = self.n.GetMap("map_request")
        # get players
        self.client_data = ClientData()
        self.server_data = self.n.GetPlayers("wall_request")

        self.network_thread = Thread(target=self.ThreadedNetwork, args=())
        self.network_thread.start()

        #stuff
        self.just_recieved_server_data = False

        # initialize map and walls
        # for wall in self.map:
            # Wall(wall.pos.x, wall.pos.y, wall.width, wall.height)

    # ---NETWORKING STUFF---
    def ThreadedNetwork(self):
        
        lastFrame = time.time()

        while True:
            currentTime = time.time()
            dt = currentTime - lastFrame
            lastFrame = currentTime

            self.client_data.dt = dt

            self.server_data = self.n.SendGet(self.client_data)
            self.just_recieved_server_data = True
            time.sleep(0.01)

    #---EVENTS---
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos.x, self.mouse_pos.y = x, y


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mouse_pos.x, self.mouse_pos.y = x, y


    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:
            self.left_clicking = True


    def on_mouse_release(self, x, y, button, modifiers):
        if button == 1:
            self.left_clicking = False
    
    def on_close(self):
        self.n.SendClose()
        self.n.Close()
        self.close()

    #---UPDATE---
    #update
    def update(self, dt, keys):  # dt is useless here only in the threaded function
        self.client_data.keys = keys
        self.client_data.left_clicking = self.left_clicking
        self.client_data.mouse_pos = self.mouse_pos
        
        if self.just_recieved_server_data is False:
            for player in self.server_data.other_players:
                player.pos = player.pos + player.vel * dt
        self.just_recieved_server_data = False

    #draw
    def on_draw(self):
        self.clear()

        our_player = self.server_data.player

        # our bullets
        for bullet in our_player.gun.bullets:
            BULLETSPRITE.position = (bullet.pos + our_player.camera).tuple()
            BULLETSPRITE.draw()
        # our player
        self.PLAYERSPRITES[our_player.image_index].position = SCREENWIDTH / 2, SCREENHEIGHT / 2
        self.PLAYERSPRITES[our_player.image_index].rotation = our_player.angle_looking
        self.PLAYERSPRITES[our_player.image_index].draw()

        # other players stuff
        for player in self.server_data.other_players:
            # other players bullets
            for bullet in player.gun.bullets:
                BULLETSPRITE.position = (bullet.pos + our_player.camera).tuple()
                BULLETSPRITE.draw()
            # other players sprites
            self.PLAYERSPRITES[player.image_index].position = (player.pos + our_player.camera).tuple()
            self.PLAYERSPRITES[player.image_index].rotation = player.angle_looking
            self.PLAYERSPRITES[player.image_index].draw()
            # other players gun
            GUNSPRITE.position = (player.pos + our_player.camera).tuple()
            GUNSPRITE.rotation = player.angle_looking
            GUNSPRITE.draw()

        # our gun
        GUNSPRITE.position = SCREENWIDTH / 2, SCREENHEIGHT / 2
        GUNSPRITE.rotation = our_player.angle_looking
        GUNSPRITE.draw()

def main():
    screen = Game(SCREENWIDTH, SCREENHEIGHT, "Game") #parameters: width, hight, title
    screen.set_vsync(True)
    keys = key.KeyStateHandler()
    screen.push_handlers(keys)
    pyglet.clock.schedule_interval(screen.update, screen.frame_rate, keys)
    pyglet.app.run()
    return 0

main()