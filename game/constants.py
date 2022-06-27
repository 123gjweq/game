import pyglet
import socket
import math

def CenterImage(image):
    image.anchor_x = math.floor(image.width / 2)
    image.anchor_y = math.floor(image.height / 2)
SCREENWIDTH = 1500
SCREENHEIGHT = 900

ADDRESS = (socket.gethostbyname(socket.gethostname()), 1234)

TIMEBETWEENSEND = .05

INJURED4 = pyglet.image.load('images/playerInjured4.png')
INJURED3 = pyglet.image.load('images/playerInjured3.png')
INJURED2 = pyglet.image.load('images/playerinjured2.png')
INJURED1 = pyglet.image.load('images/playerinjured1.png')
INJURED0 = pyglet.image.load('images/playerinjured0.png')
CenterImage(INJURED4)
CenterImage(INJURED3)
CenterImage(INJURED2)
CenterImage(INJURED1)
CenterImage(INJURED0)
INJURED4SPRITE = pyglet.sprite.Sprite(INJURED4, 0, 0)
INJURED3SPRITE = pyglet.sprite.Sprite(INJURED3, 0, 0)
INJURED2SPRITE = pyglet.sprite.Sprite(INJURED2, 0, 0)
INJURED1SPRITE = pyglet.sprite.Sprite(INJURED1, 0, 0)
INJURED0SPRITE = pyglet.sprite.Sprite(INJURED0, 0, 0)
REFERENCEPOINT = pyglet.image.load('images/reference.png')