import pickle, time
from player import Player

from reusableClasses.collisions import Collision

players = []

def ThreadedClient(conn, ID):
    player = Player((0, 0))

    id_get = pickle.loads(conn.recv(1000))
    if id_get == "ID":
        conn.send(pickle.dumps(ID))

    keys, dt, mouse_pos, is_leftclicking = pickle.loads(conn.recv(10000))
    player.Update(keys, dt, mouse_pos, is_leftclicking)
    players.append(
        [player.poses,
        player.vel,
        player.health,
        player.angle_looking,
        player.image_index,
        player.gun]
    )

    conn.sendall(pickle.dumps(players))

    while True:
        client_player = pickle.loads(conn.recv(10000))

        if client_player == "Quit":
            conn.close()
            print(f"Closed connection with ID:{ID}") 
            break

        keys, dt, mouse_pos, is_leftclicking = client_player
        player.Update(keys, dt, mouse_pos, is_leftclicking)

        players[ID] = (player.poses,
        player.vel,
        player.health,
        player.angle_looking,
        player.image_index,
        player.gun,
        player.camera,
        time.time())

        conn.sendall(pickle.dumps(players))

    return 0