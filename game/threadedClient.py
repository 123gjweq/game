import pickle
import time
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

    def __init__(self, conn, ID):
        self.walls = LoadMap("maps/testMap.txt")
        Gun.walls.append(self.walls)

        self.client_data = ClientData()
        self.server_data = ServerData()


        # create everything before the threads start!
        self.threaded_game = Thread(target=self.ThreadedGame, args=(conn, ID))
        self.threaded_game.start()

    def ThreadedGame(self, conn, ID):
        # make player
        ThreadedClient.players.append(Player(Vector2(1000, 2000))) # this vector is where you spawn
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

            if self.client_data == "Quit":
                conn.close()
                print(f"Closed connection with ID:{ID}") 
                ThreadedClient.players.remove(ThreadedClient.players[ID])
                break
            
            our_player = ThreadedClient.players[ID]
            our_player.Update(self.client_data)

            if our_player.health <= 0:
                conn.send(pickle.dumps("You Died"))
                our_player.pos = Vector2(-1000, -1000)
                ThreadedClient.players.remove(ThreadedClient.players[ID])
                print(f"Player Died with ID:{ID}")
                break

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
                    if player != our_player:
                        if Collision.PointOnCircle(bullet.pos, player.pos, 25):
                            player.health -= our_player.gun.damage
                            if player.health <= 0:
                                our_player.kills += 1
                                if not our_player.kills > 9:
                                    our_player.gun.ChangeStats(Gun.upgrades[our_player.kills])
                            our_player.gun.bullets.remove(bullet)
                            break

            other_players = ThreadedClient.players[0:]
            other_players.pop(ID)
            self.server_data.other_players = other_players

            conn.send(pickle.dumps(self.server_data))