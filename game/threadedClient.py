import pickle
import time
import random
from threading import Thread

from loadmap import LoadMap
from player import Player
from gun import Gun
from threading import Thread

from sentStuff import *

from reusableClasses.vector2 import Vector2
from reusableClasses.collisions import Collision

class ThreadedClient:
    players = []

    spawningPoints =   [Vector2(x[0], x[1]) for x in [ (2739, 263),
                                                                (3360, 2070),
                                                                (1449, 1017),
                                                                (129, 419),
                                                                (1716, 2090),
                                                                (2963, 1469),
                                                                (1442, 2582),
                                                                (2315, 2335),
                                                                (1496, 307),
                                                                (3001, 181),
                                                                (2310, 895),]]

    def __init__(self, conn, ID):
        self.walls = LoadMap("maps/map.txt")
        Gun.walls.append(self.walls)

        self.client_data = ClientData()
        self.server_data = ServerData()

        self.dead = False

        self.intialSpawnPoint = Vector2(random.randrange(3150, 3150 + 250), random.randint(300, 300 + 200)) # 3150, 300, 250, 200

        # create everything before the threads start!
        self.threaded_game = Thread(target=self.ThreadedGame, args=(conn, ID))
        self.threaded_game.start()

        self.justSpawned = True

    def ThreadedGame(self, conn, ID):
        # make player
        ThreadedClient.players.append(Player(self.intialSpawnPoint)) # this vector is where you spawn
        other_players = ThreadedClient.players[0:]
        other_players.pop(ID)
        server_data = ServerData(ThreadedClient.players[ID], other_players)

        # send server's ID to client
        id_request = pickle.loads(conn.recv(100))
        if id_request == "ID":
            conn.send(pickle.dumps(ID))
        # send wall map to player
        map_request = pickle.loads(conn.recv(100))
        if map_request == "map_request":
            conn.send(pickle.dumps(self.walls))
        # send players to client
        wall_request = pickle.loads(conn.recv(100))
        if wall_request == "wall_request":
            conn.send(pickle.dumps(server_data))
        
        Player.walls = self.walls
        Gun.walls = self.walls

        while True:
            self.client_data = pickle.loads(conn.recv(10000))

            if self.client_data.username:
                ThreadedClient.players[ID].username = self.client_data.username

            if self.client_data.joinedGame and self.justSpawned:
                ThreadedClient.players[ID].pos = random.choice(ThreadedClient.spawningPoints)
                self.justSpawned = False

            # if the player clicks respawn button
            if self.dead and self.client_data.respawn:
                # set player stats back to default
                our_player = ThreadedClient.players[ID]
                our_player.pos = random.choice(ThreadedClient.spawningPoints)
                our_player.kills = 0
                self.dead = False

            # if the player x's out of the game
            if self.client_data == "Quit":
                conn.close()
                print(f"Closed connection with ID:{ID}") 
                ThreadedClient.players[ID] = None
                break
            
            our_player = ThreadedClient.players[ID]
            if not self.dead:
                our_player.Update(self.client_data)

            if our_player.health <= 0:
                self.dead = True
                conn.send(pickle.dumps("You Died"))
                our_player.pos = Vector2(-1000, -1000)
                our_player.health = 100
                print(f"Player Died with ID:{ID}")

            # update our_player bullets
            for bullet in our_player.gun.bullets:
                # bullet moves
                bullet.Move(self.client_data.dt * 60)

                # check if bullet should die
                if bullet.should_die:
                    our_player.gun.bullets.remove(bullet)
                    continue

                # check if bullet hit any other player
                for player in ThreadedClient.players:
                    if player != our_player and player != None:
                        if Collision.PointOnCircle(bullet.pos, player.pos, 25):
                            player.health -= our_player.gun.damage
                            player.time_last_hit = time.time()
                            if player.health <= 0:
                                our_player.kills += 1
                                our_player.health += 50
                                if not our_player.kills > 9:
                                    our_player.gun.ChangeStats(Gun.upgrades[our_player.kills])
                            our_player.gun.bullets.remove(bullet)
                            break

            our_player.health = min(our_player.health, our_player.max_health)

            other_players = ThreadedClient.players[0:]
            other_players.pop(ID)

            self.server_data.player = our_player
            self.server_data.other_players = other_players

            conn.send(pickle.dumps(self.server_data))
            #print(ThreadedClient.players)