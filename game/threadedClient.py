import pickle

from loadmap import LoadMap
from player import Player
from sentStuff import *

from reusableClasses.vector2 import Vector2

players = []
walls = LoadMap("maps/testMap.txt")

def ThreadedClient(conn, ID):
    # make player
    # spawn at anyhwere else other than (0, 0) and you will get bug fix camera for later
    players.append(Player(Vector2(0, 0)))
    other_players = players[0:]
    other_players.pop(ID)
    server_data = ServerData(players[ID], other_players)

    # send server's ID to client
    id_request = pickle.loads(conn.recv(100))
    if id_request == "ID":
        conn.send(pickle.dumps(ID))
    # send wall map to player
    map_request = pickle.loads(conn.recv(100))
    if map_request == "map_request":
        conn.send(pickle.dumps(walls))
    # send players to client
    wall_request = pickle.loads(conn.recv(100))
    if wall_request == "wall_request":
        conn.send(pickle.dumps(server_data))

    while True:
        client_data = pickle.loads(conn.recv(10000))

        if client_data == "Quit":
            conn.close()
            print(f"Closed connection with ID:{ID}") 
            break
        
        players[ID].Update(client_data.keys, client_data.dt, client_data.left_clicking, client_data.mouse_pos)


        other_players = players[0:]
        other_players.pop(ID)

        server_data.player = players[ID]
        server_data.other_players = other_players
        conn.send(pickle.dumps(server_data))

    return 0