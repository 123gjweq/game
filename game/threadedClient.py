import pickle

players = []

def ThreadedClient(conn, ID):
    player = pickle.loads(conn.recv(10000))
    conn.sendall(pickle.dumps(players))
    players.append(player)

    while True:
        client_player = pickle.loads(conn.recv(10000))

        if client_player == "Quit":
            conn.close()
            print(f"Closed connection with ID:{ID}") 
            break

        players[ID] = client_player

        other_players = players[0:]
        other_players.pop(ID)

        conn.send(pickle.dumps(other_players))

    return 0 