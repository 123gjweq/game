import pickle
import time
from threading import Thread

from loadmap import LoadMap
from player import Player
from threading import Thread

from sentStuff import *

from reusableClasses.vector2 import Vector2
from reusableClasses.collisions import Collision

class ThreadedClient:
    players = []

    def __init__(self, conn, ID):
        self.walls = LoadMap("maps/testMap.txt")

        self.client_data = ClientData()
        self.server_data = ServerData()


        # create everything before the threads start!
        self.threaded_game = Thread(target=self.ThreadedGame, args=(conn, ID))
        self.threaded_game.start()

        #self.threaded_client_data = Thread(target=self.ThreadedClientData, args=(conn, ID))
        #self.threaded_client_data.start()

    def ThreadedClientData(self, conn, ID):
        pass

    def ThreadedGame(self, conn, ID):
        # make player
        # spawn at anyhwere else other than (0, 0) and you will get bug fix camera for later
        ThreadedClient.players.append(Player(Vector2(0, 0)))
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

        while True:
            self.client_data = pickle.loads(conn.recv(10000))

            if self.client_data == "Quit":
                conn.close()
                print(f"Closed connection with ID:{ID}") 
                break
            
            ThreadedClient.players[ID].Update(self.client_data.keys, self.client_data.dt, self.client_data.left_clicking, self.client_data.mouse_pos)

            our_player = ThreadedClient.players[ID]

            # check if bullets hits the player
            other_players = ThreadedClient.players[0:]
            other_players.remove(ThreadedClient.players[ID])


            other_players = ThreadedClient.players[0:]
            other_players.pop(ID)

            self.server_data.player = ThreadedClient.players[ID]
            self.server_data.other_players = other_players
            conn.send(pickle.dumps(self.server_data))