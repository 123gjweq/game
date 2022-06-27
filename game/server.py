import socket
from threading import Thread
from threadedClient import ThreadedClient
from constants import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDRESS)

print("Server started waiting for people")

s.listen()

ID = 0
while True:
    conn, addr = s.accept()

    print(f"player {addr} connected")

    clientThread = Thread(target=ThreadedClient, args=(conn, ID))
    ID += 1
    clientThread.start()