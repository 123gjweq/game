import pyglet
from pyglet.window import key
import pickle
import time
from threading import Thread
from player import Player
from network import Network
from reusableClasses.vector2 import Vector2
from constants import *

class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        self.frame_rate = 1/120.0
        self.mouse_pos = Vector2()
        self.is_leftclicking = False

        self.PLAYERSPRITES = [INJURED4SPRITE, INJURED3SPRITE, INJURED2SPRITE, INJURED1SPRITE, INJURED0SPRITE]

        #player stuff
        self.dt = 0
        self.keys = {key.W: False, key.A: False, key.S: False, key.D: False}

        # connection
        self.n = Network()
        self.ID = self.n.SendID()
        self.other_players = self.n.SendGet((self.keys, self.dt, self.mouse_pos, self.is_leftclicking))
        self.player = self.other_players[self.ID]
        self.pos_counters = [self.ID] * len(self.other_players) #this will tell when we just recieved a packet
        #this is for making it smooth. I store players other position, check if it is equal, and then upadte vel

        networkThread = Thread(target=self.ThreadedNetwork, args=())
        networkThread.start()
        time.sleep(.2)

    def ThreadedNetwork(self):
        while True:
            t1 = time.time()
            self.other_players = self.n.SendGet((self.keys, self.dt, self.mouse_pos, self.is_leftclicking))
            self.player = self.other_players[self.ID]
            self.calculate_pos_counters()

            time_to_send = time.time() - t1
            if TIMEBETWEENSEND - time_to_send > 0:
                time.sleep(TIMEBETWEENSEND - time_to_send)
            else:
                time.sleep(TIMEBETWEENSEND)

    def calculate_pos_counters(self):
        for i in range(len(self.pos_counters)):
            self.pos_counters[i] = 0
        if len(self.pos_counters) < len(self.other_players):
            self.pos_counters.append(0)

    def interval_pos_counters(self):
        for i in range(len(self.pos_counters)):
            self.pos_counters[i] += 1

    #events
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos.x, self.mouse_pos.y = x, y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mouse_pos.x, self.mouse_pos.y = x, y

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:
            self.is_leftclicking = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == 1:
            self.is_leftclicking = False
    
    def on_close(self):
        self.n.SendClose()
        self.n.Close()
        self.close()

        
    #update
    def update(self, dt, keys):
        self.dt = dt
        self.keys = keys

        

    #draw
    def on_draw(self):
        self.clear()
        camera = self.player[0][self.pos_counters[self.ID]]

        # other players
        for index, player in enumerate(self.other_players):

            #we add a list to other play positions to keep track of other players
            self.PLAYERSPRITES[player[4]].x, self.PLAYERSPRITES[player[4]].y =\
            player[0][self.pos_counters[index]].x + self.player[6].x - camera.x, player[0][self.pos_counters[index]].y + self.player[6].y - camera.y
            self.PLAYERSPRITES[player[4]].draw()
            # other players guns
            GUNSPRITE.x, GUNSPRITE.y = player[0][self.pos_counters[index]].x + self.player[6].x - camera.x, player[0][self.pos_counters[index]].y + self.player[6].y - camera.y
            GUNSPRITE.rotation = player[3]
            GUNSPRITE.draw()
            # other players bullets
            for bullet in player[5].bullets:
                bullet.pos += (bullet.dir * bullet.speed) * self.dt * 60
                BULLETSPRITE.x, BULLETSPRITE.y = bullet.pos.x + self.player[6].x, bullet.pos.y + self.player[6].y
                BULLETSPRITE.draw()

        # reference point
        REFERENCEPOINT.blit(self.player[6].x - camera.x, self.player[6].y - camera.y)
        self.interval_pos_counters()


def main():
    screen = Game(SCREENWIDTH, SCREENHEIGHT, "Game") #parameters: width, hight, title
    screen.set_vsync(True)

    keys = key.KeyStateHandler()
    screen.push_handlers(keys)

    pyglet.clock.schedule_interval(screen.update, screen.frame_rate, keys)
    pyglet.app.run()

    return 0

main()