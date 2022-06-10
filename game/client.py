import pyglet
from pyglet.window import key
import pickle
import time
from threading import Thread
from player import Player
from network import Network
from vector2 import Vector2
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
        self.player = Player(Vector2(0, 0))

        # connection
        self.n = Network()
        self.other_players = self.n.SendGet(self.player)

        networkThread = Thread(target=self.ThreadedNetwork, args=())
        networkThread.start()

    def ThreadedNetwork(self):
        while True:
            self.other_players = self.n.SendGet(self.player)
            time.sleep(0.05)

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
        self.player.Update(keys, dt, self.is_leftclicking, self.mouse_pos)

    #draw
    def on_draw(self):
        self.clear()
        # our player
        self.PLAYERSPRITES[self.player.image_index].x, self.PLAYERSPRITES[self.player.image_index].y = SCREENWIDTH / 2, SCREENHEIGHT / 2
        self.PLAYERSPRITES[self.player.image_index].draw()
        # other players
        for player in self.other_players:
            self.PLAYERSPRITES[player.image_index].x, self.PLAYERSPRITES[player.image_index].y = player.pos.x + self.player.camera.x, player.pos.y + self.player.camera.y
            self.PLAYERSPRITES[player.image_index].draw()
        # reference point
        REFERENCEPOINT.blit(self.player.camera.x, self.player.camera.y)


def main():
    screen = Game(SCREENWIDTH, SCREENHEIGHT, "Game") #parameters: width, hight, title
    screen.set_vsync(True)

    keys = key.KeyStateHandler()
    screen.push_handlers(keys)

    pyglet.clock.schedule_interval(screen.update, screen.frame_rate, keys)
    pyglet.app.run()

    return 0

main()