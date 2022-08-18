"""
These classes are what is sent to the server, and what is sent back to the client
"""

from pyglet.window import key

from reusableClasses.vector2 import Vector2

class ClientData:
    def __init__(self, keys={key.W:False, key.A:False, key.S:False, key.D:False, key.R:False}, left_clicking=False, mouse_pos=Vector2(), dt=0.83333333):
        self.keys = keys
        self.left_clicking = left_clicking
        self.mouse_pos = mouse_pos
        self.dt = dt
        self.angle_looking = 0
        self.last_two_angles = [0, 0]
        self.respawn = False
        self.joinedGame = False
        self.username = ""

class ServerData:
    def __init__(self, player=None, other_players=None):
        self.player = player
        self.other_players = other_players