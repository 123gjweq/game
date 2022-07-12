import socket
import pickle

from constants import ADDRESS

class Network:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(ADDRESS)
        print("Connected to server")

    def GetID(self, ID):  # ID should be "ID"
        self.s.send(pickle.dumps(ID))
        return pickle.loads(self.s.recv(100))

    def GetMap(self, map_request):  # map_request should be "map_request"
        self.s.send(pickle.dumps(map_request))
        return pickle.loads(self.s.recv(10000))

    def GetPlayers(self, player_request): # player_request should be "player_request"
        self.s.send(pickle.dumps(player_request))
        return pickle.loads(self.s.recv(10000))

    def SendGet(self, clientData):
        self.s.send(pickle.dumps(clientData))
        return pickle.loads(self.s.recv(10000))

    def SendClose(self):
        self.s.send(pickle.dumps("Quit"))

    def Close(self):
        self.s.close()