from turtle import window_width
import pyglet

from reusableClasses.collisions import Collision

class InputBox():
    def __init__(self, pos, width, height, maxCharacterLength=10):
        self.pos = pos
        self.width = width
        self.height = height

        self.active = False

        self.text = ''

        self.maxCharacterLength = maxCharacterLength

    def OnClick(self, mousePos):
        if Collision.PointOnRect(mousePos, self.pos, self.width, self.height):
            self.active = True
        else:
            self.active = False

    def OnText(self, text):
        # add text to input box
        self.text += text
        if len(self.text) > self.maxCharacterLength:
            self.text = self.text[0:self.maxCharacterLength]

    def OnBackspace(self):
        # if the string is empty you can't delete characters in input box
        if self.text != '':
            self.text = self.text.rstrip(self.text[-1])