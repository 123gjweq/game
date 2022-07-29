import pyglet
import socket
import math
from reusableClasses.vector2 import Vector2

def CenterImage(image):
    image.anchor_x = math.floor(image.width / 2)
    image.anchor_y = math.floor(image.height / 2)
    
SCREENWIDTH = 1500
SCREENHEIGHT = 900

ADDRESS = ("192.168.1.132", 1234)

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
GUNIMAGE = pyglet.image.load('images/gun.png')
GUNIMAGE.anchor_x = math.floor(GUNIMAGE.width / 2)
GUNIMAGE.anchor_y = 5
GUNSPRITE = pyglet.sprite.Sprite(GUNIMAGE, 0, 0)

BULLETIMAGE = pyglet.image.load('images/bullet.png')
CenterImage(BULLETIMAGE)
BULLETSPRITE = pyglet.sprite.Sprite(BULLETIMAGE, 0, 0)