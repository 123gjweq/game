import socket
import pickle

from constants import ADDRESS

class Network:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(ADDRESS)
        print("Connected to server")

    def SendGet(self, clientData):
        self.s.send(pickle.dumps(clientData))
        return pickle.loads(self.s.recv(10000))

    def SendClose(self):
        self.s.send(pickle.dumps("Quit"))

    def Close(self):
        self.s.close()