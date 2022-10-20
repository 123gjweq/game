import pyglet
from pyglet.window import key
from threading import Thread
from random import randrange
from audio import Audio
import time

from player import Player
from network import Network
from wall import Wall
from sentStuff import *
from constants import *

from reusableClasses.vector2 import Vector2
from reusableClasses.collisions import Collision
from reusableClasses.inputBox import InputBox


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

        self.died = False

        self.network_thread = Thread(target=self.ThreadedNetwork, args=())
        self.network_thread.start()

        #player prediction
        self.just_recieved_server_data = False
        self.is_playing = False

        # initialize map and walls
        for wall in self.map:
            Wall(wall.pos.x, wall.pos.y, wall.width, wall.height)

        self.usernameBox = InputBox(Vector2(750 - 300/2, 290 - 75/2), 300, 75)

        self.username = ''
        self.ammo_label = pyglet.text.Label(f"string",
                            font_name='serif',
                            font_size=45,
                            x=1350, y=100,
                            anchor_x='center', anchor_y='center',
                            color=(181,230,29, 255))

        self.username_label = pyglet.text.Label(f"string",
                            font_name='serif',
                            font_size=15,
                            x=1350, y=100,
                            anchor_x='center', anchor_y='center',
                            color=(181,230,29, 255))

        self.kills_label = pyglet.text.Label(f"string",
                            font_name='serif',
                            font_size=70,
                            x=830, y=790,
                            anchor_x='center', anchor_y='center',
                            color=(181,230,29, 255))

        self.kills_label.opacity = 150

        self.audio = Audio()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.BACKSPACE:
            self.usernameBox.OnBackspace()

    def on_text(self, text):
        if not self.is_playing:
            self.usernameBox.OnText(text)

    def RemoveNone(self, players):
        new_players = []

        for player in players:
            if player != None:
                new_players.append(player)
        
        return new_players

    # ---NETWORKING STUFF---
    def ThreadedNetwork(self):
        
        lastFrame = time.time()

        while True:
            currentTime = time.time()
            dt = currentTime - lastFrame
            lastFrame = currentTime

            self.client_data.dt = dt

            data = self.n.SendGet(self.client_data)

            if data == "You Died":
                self.died = True
                self.client_data.respawn = False
            else:
                self.server_data = data
                self.server_data.other_players = self.RemoveNone(data.other_players)
            
            for player in self.server_data.other_players:
                if player.sound_info != None:
                    sound_player = self.audio.GetAvailablePlayer()
                    if sound_player != False:
                        sound_player.queue(Audio.dict_of_sounds[player.sound_info[0]])
                        sound_player.volume = 1.0
                        print("Playing sound")
                        sound_player.play()

            self.just_recieved_server_data = True

    #---EVENTS---
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos.x, self.mouse_pos.y = x, y


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mouse_pos.x, self.mouse_pos.y = x, y


    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:
            self.left_clicking = True

            self.usernameBox.OnClick(Vector2(x, y))

    def on_mouse_release(self, x, y, button, modifiers):
        if button == 1:
            self.left_clicking = False

            if self.died:
                if Collision.PointOnRect(self.mouse_pos, Vector2(675, 118), 150, 65):
                    self.client_data.respawn = True
                    self.died = False

            if not self.is_playing:
                if Collision.PointOnRect(self.mouse_pos, Vector2(675, 118), 150, 65):
                    self.username = self.usernameBox.text
                    self.client_data.username = self.username  # professionally:    set username to username
                    self.is_playing = True
                    self.client_data.joinedGame = True
    
    def on_close(self):
        self.n.SendClose()
        time.sleep(.5)
        self.n.Close()
        self.close()

    #update helper function helps predict stuf so it doesnt look like running at 10 fps
    def player_prediction(self, dt):
        #update the rotation client-side (it make is look less girry)
        self.client_data.angle_looking = \
        math.degrees((self.mouse_pos - Vector2(SCREENWIDTH / 2, SCREENHEIGHT / 2)).angle) + 90
        #update last two angles that are looked
        self.client_data.last_two_angles.append(self.client_data.angle_looking)
        self.client_data.last_two_angles.pop(0)

        if self.just_recieved_server_data is False:
            for player in self.server_data.other_players:
                player.pos += player.vel * dt * 60
                #smooth angle predictions
                player.angle_looking += (player.last_two_angles[1] - player.last_two_angles[0]) * .8
            player = self.server_data.player
            player.pos += player.vel * (dt * 60)
            player.camera.pos -= player.vel * (dt * 60)
        else:
            #This will make sure the players are in sync
            player = self.server_data.player
            player.pos -= player.vel * (player.dt * 30)
            player.camera.pos += player.vel * (player.dt * 30)

    #---UPDATE---
    #update
    def update(self, dt, keys):
        self.client_data.keys = keys
        self.client_data.left_clicking = self.left_clicking
        self.client_data.mouse_pos = self.mouse_pos
        
        self.player_prediction(dt)

        self.just_recieved_server_data = False

    #draw
    def on_draw(self):
        self.clear()

        if self.is_playing:
            player_spectating = self.server_data.player if (not self.died or self.server_data.other_players == []) else self.server_data.other_players[0]

            # our bullets
            for bullet in player_spectating.gun.bullets:
                BULLETSPRITE.position = (bullet.pos + player_spectating.camera.offset).tuple()
                BULLETSPRITE.draw()
            # our player
            if not self.died:
                self.PLAYERSPRITES[player_spectating.image_index].position = SCREENWIDTH / 2, SCREENHEIGHT / 2
                self.PLAYERSPRITES[player_spectating.image_index].rotation = self.client_data.angle_looking

                self.username_label.text = self.username
                self.username_label.x = SCREENWIDTH / 2
                self.username_label.y = SCREENHEIGHT / 2 + 55

                self.PLAYERSPRITES[player_spectating.image_index].draw()
                self.username_label.draw()

            # walls
            for i in range(0, len(Wall.wallBatch), 1):
                # update wall position with camera then draw
                Wall.wallBatch[i].position = (Wall.walls[i].pos + player_spectating.camera.offset).tuple()
                Wall.wallBatch[i].draw()

            # other players stuff
            for player in self.server_data.other_players:
                tup = (player.pos + player_spectating.camera.offset).tuple()
                # other players bullets
                for bullet in player.gun.bullets:
                    BULLETSPRITE.position = (bullet.pos + player_spectating.camera.offset).tuple()
                    BULLETSPRITE.draw()
                # other players sprites
                self.PLAYERSPRITES[player.image_index].position = tup
                self.PLAYERSPRITES[player.image_index].rotation = player.angle_looking

                self.username_label.text = player.username
                self.username_label.x = tup[0]
                self.username_label.y = tup[1] + 55

                self.PLAYERSPRITES[player.image_index].draw()
                self.username_label.draw()
                # other players gun
                GUNSPRITE.position = (player.pos + player_spectating.camera.offset).tuple()
                GUNSPRITE.rotation = player.angle_looking
                GUNSPRITE.draw()

            # our gun
            if not self.died:
                GUNSPRITE.position = SCREENWIDTH / 2, SCREENHEIGHT / 2
                GUNSPRITE.rotation = self.client_data.angle_looking
                GUNSPRITE.draw()

            # top killer
            topKiller = self.server_data.player
            for player in self.server_data.other_players:
                if player.kills > topKiller.kills:
                    topKiller = player
            self.username_label.text = topKiller.username
            self.username_label.x, self.username_label.y = 700, 830
            self.username_label.font_size = 25
            self.username_label.opacity = 150

            self.kills_label.text = str(topKiller.kills)
            

            TOPKILLERSPRITE.draw()
            self.username_label.draw()
            self.kills_label.draw()
            self.username_label.font_size = 15
            self.username_label.opacity = 255

            # draw ammo text
            self.ammo_label.text = f"{self.server_data.player.gun.bullets_left}|{self.server_data.player.gun.clip_size}"
            self.ammo_label.bold = True
            self.ammo_label.draw()

            if self.died:
                LIMAGESPRITE.draw()
                if Collision.PointOnRect(self.mouse_pos, Vector2(675, 118), 150, 65):
                    RESPAWNONHOVERSPRITE.draw()
                else:
                    RESPAWNOFFHOVERSPRITE.draw()
        else:
            MAINSCREENSPRITE.draw()
            # button
            # if you click play button on start of game
            if Collision.PointOnRect(self.mouse_pos, Vector2(675, 118), 150, 65):
                ENTERGAMEBUTTONONHOVERSPRITE.draw()
            else:
                ENTERGAMEBUTTONOFFHOVERSPRITE.draw()
            # username image, text
            if self.usernameBox.active is False:
                INPUTBOXIMAGENOTACTIVESPRITE.draw()
            else:
                INPUTBOXIMAGEACTIVESPRITE.draw()
            label = pyglet.text.Label(self.usernameBox.text,
                            font_name='serif',
                            font_size=30,
                            x=750, y=300,
                            anchor_x='center', anchor_y='center',
                            color=(181,230,29, 255))
            label.bold = True
            label.draw()


def main():
    screen = Game(SCREENWIDTH, SCREENHEIGHT, "Game") #parameters: width, hight, title
    screen.set_vsync(True)
    keys = key.KeyStateHandler()
    screen.push_handlers(keys)
    pyglet.clock.schedule_interval(screen.update, screen.frame_rate, keys)
    pyglet.app.run()
    return 0

main()