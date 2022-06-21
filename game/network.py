import socket
import pickle

from constants import ADDRESS

class Network:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(ADDRESS)
        print("Connected to server")

    def SendID(self):
        self.s.send(pickle.dumps("ID"))
        return pickle.loads(self.s.recv(1000))

    def SendGet(self, clientData):
        self.s.send(pickle.dumps(clientData))
        return pickle.loads(self.s.recv(60000))

    def SendClose(self):
        self.s.send(pickle.dumps("Quit"))

    def Close(self):
        self.s.close()