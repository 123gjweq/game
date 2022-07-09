import pyglet
from pyglet.window import key
from random import randrange
import time
from threading import Thread
from player import Player
from network import Network
from reusableClasses.vector2 import Vector2
from wall import Wall
from constants import *


class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        #pygame stuff
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
        self.other_players = self.n.SendGet(self.player) #send player
        self.map = self.n.SendMap("mapRequest") #request map
        networkThread = Thread(target=self.ThreadedNetwork, args=()) #a threaded connection between client and server
        networkThread.start()

        #initialize map and walls
        for wall in self.map:
            Wall(wall.pos.x, wall.pos.y, wall.width, wall.height)

        #player prediction stuff
        self.dt = 1 #delta time
        self.loopps = [] #list of other players' (previous) packets
        self.loopp = [] #list of other players' positions
        self.other_player_predictions = [[]] * len(self.other_players) #list of other players predicted positions
        self.other_player_counters = 0 #increment self.other_player_predictions


    def ThreadedNetwork(self):
        while True:
            self.other_players = self.n.SendGet(self.player)
            for index, player in enumerate(self.other_players):
                if len(self.loopps) < index + 1:
                    self.loopps.append([(player.pos, time.time() - 1) for i in range(10)])
                    self.loopp.append([(player.pos, time.time())])
                self.loopps[index].insert(0, (player.pos, time.time()))
                self.loopps[index].pop()
            

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
    def update_the_packets(self, player_index, packet_index):
        last_packet = self.loopp[player_index][0]
        new_packet = self.loopps[player_index][packet_index]
        if (new_packet[0] - last_packet[0]).length <= 6:
            if self.other_players[player_index].vel.length < 2:
                estimated_position = self.other_players[player_index].vel.GetNormalized() * 5 + last_packet[0]
                self.loopp[player_index].insert(0, (estimated_position, 0))
            else:
                self.loopp[player_index].insert(0, last_packet)
            return
        direction = (new_packet[0] - last_packet[0]).GetNormalized()
        guess = 1
        while True:
            estimated_position = direction * guess * 5 + last_packet[0]
            self.loopp[player_index].insert(0, (estimated_position, 0))
            guess += 1
            if abs(new_packet[0].length) - abs(estimated_position.length) < 6.5:
                break

    #update
    def update(self, dt, keys):
        self.dt = dt
        self.player.Update(keys, dt, self.is_leftclicking, self.mouse_pos)

    #draw
    def on_draw(self):
        
        self.clear()

        #first and foremost, we want to draw walls
        for i in range(0, len(Wall.wallBatch), 1):
            # update wall pos with camera
            wall = Wall.walls[i]
            #this if statement and the next check if the wall is on the screen.
            if wall.init_x < self.player.pos.x + 750 and wall.init_x + wall.width > self.player.pos.x - 750:
                if wall.init_y < self.player.pos.y + 450 and wall.init_y + wall.height > self.player.pos.y - 450:
                    Wall.wallBatch[i].x, Wall.wallBatch[i].y = Wall.walls[i].pos.x + self.player.camera.x, Wall.walls[i].pos.y + self.player.camera.y
                    Wall.wallBatch[i].draw()

        self.PLAYERSPRITES[self.player.image_index].x, self.PLAYERSPRITES[self.player.image_index].y = 750, 450
        self.PLAYERSPRITES[self.player.image_index].draw()

        GUNSPRITE.x, GUNSPRITE.y = SCREENWIDTH / 2, SCREENHEIGHT / 2
        GUNSPRITE.rotation = self.player.angle_looking
        GUNSPRITE.draw()
        
        # our bullets
        for bullet in self.player.gun.bullets:
            BULLETSPRITE.x, BULLETSPRITE.y = bullet.pos.x + self.player.camera.x, bullet.pos.y + self.player.camera.y
            BULLETSPRITE.draw()


        # other players
        for index, player in enumerate(self.other_players):
            if len(self.loopp[index]) == 1:
                self.update_the_packets(index, 0)

            for bullet in player.gun.bullets:
                # "predict" the bullet pos but we already know where its going to be next frame
                bullet.pos += (bullet.dir * bullet.speed) * self.dt * 60
                BULLETSPRITE.x, BULLETSPRITE.y = bullet.pos.x + self.player.camera.x, bullet.pos.y + self.player.camera.y
                BULLETSPRITE.draw()

            player_pos = self.loopp[index][-1][0].x + self.player.camera.x, self.loopp[index][-1][0].y + self.player.camera.y

            self.PLAYERSPRITES[player.image_index].x, self.PLAYERSPRITES[player.image_index].y = player_pos
            
            self.PLAYERSPRITES[player.image_index].draw()
            self.loopp[index].pop()

            GUNSPRITE.x, GUNSPRITE.y = player_pos
            GUNSPRITE.rotation = player.angle_looking
            GUNSPRITE.draw()
            # other players bullet


def main():
    screen = Game(SCREENWIDTH, SCREENHEIGHT, "Game") #parameters: width, hight, title
    screen.set_vsync(True)
    keys = key.KeyStateHandler()
    screen.push_handlers(keys)
    pyglet.clock.schedule_interval(screen.update, screen.frame_rate, keys)
    pyglet.app.run()
    return 0
main()