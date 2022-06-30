import pyglet
from pyglet.window import key
from random import randrange
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
        self.player = Player(Vector2(0, 0))
        # connection
        self.n = Network()
        self.other_players = self.n.SendGet(self.player)
        self.other_player_predictions = [[]] * len(self.other_players)
        self.other_player_counters = 0
        #this is for making it smooth. I store players other position, check if it is equal, and then upadte vel
        networkThread = Thread(target=self.ThreadedNetwork, args=())
        networkThread.start()
        self.dt = 1
        self.time_measuerment = 0


    def ThreadedNetwork(self):
        while True:
            self.other_players = self.n.SendGet(self.player)

            if time.time() - self.time_measuerment > TIMEBETWEENSEND:
                self.player_prediction()
                self.other_player_counters = 0
                self.time_measuerment = time.time()
            

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



    #player rediction stuff
    def player_prediction(self):
        for player in range(len(self.other_players)):
            cur_player = self.other_players[player]
            self.new_player_prediction_update()
            self.other_player_predictions[player] = []
            for i in range(int(TIMEBETWEENSEND * 80 * 60 * self.dt)):
                self.other_player_predictions[player].append(cur_player.pos + cur_player.lvel * i)

    def new_player_prediction_update(self):
        if len(self.other_players) > len(self.other_player_predictions):
            self.other_player_predictions.append([])

    #update
    def update(self, dt, keys):
        self.dt = dt
        self.player.Update(keys, dt, self.is_leftclicking, self.mouse_pos)

    #draw
    def on_draw(self):
        self.clear()
        self.new_player_prediction_update()

        REFERENCEPOINT.blit(self.player.camera.x, self.player.camera.y)
        # our player
        self.PLAYERSPRITES[self.player.image_index].x, self.PLAYERSPRITES[self.player.image_index].y =SCREENWIDTH / 2, SCREENHEIGHT / 2
        self.PLAYERSPRITES[self.player.image_index].draw()
        # other players
        for index, player in enumerate(self.other_players):
            if self.other_player_counters - 1 <= len(self.other_player_predictions[index]):
                cur_pos = self.other_player_predictions[index][self.other_player_counters].x + self.player.camera.x,\
                self.other_player_predictions[index][self.other_player_counters].y + self.player.camera.y
            else:
                cur_pos = self.other_player_predictions[index][-1].x + self.player.camera.x,\
                self.other_player_predictions[index][-1].y + self.player.camera.y

            self.PLAYERSPRITES[player.image_index].x, self.PLAYERSPRITES[player.image_index].y = cur_pos
            
            self.PLAYERSPRITES[player.image_index].draw()
        # reference point
        REFERENCEPOINT.blit(self.player.camera.x, self.player.camera.y)

        if len(self.other_player_predictions) > 0:
            if len(self.other_player_predictions[0]) > self.other_player_counters + 1:
                self.other_player_counters += 1


def main():
    screen = Game(SCREENWIDTH, SCREENHEIGHT, "Game") #parameters: width, hight, title
    screen.set_vsync(True)
    keys = key.KeyStateHandler()
    screen.push_handlers(keys)
    pyglet.clock.schedule_interval(screen.update, screen.frame_rate, keys)
    pyglet.app.run()
    return 0
main()