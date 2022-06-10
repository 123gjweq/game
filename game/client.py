import pyglet
from player import Player
from pyglet.window import key
from vector2 import Vector2
from constants import *

class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        self.frame_rate = 1/120.0

        #player stuff
        self.player = Player(Vector2(0, 0))

    #events
    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, buttom, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    #update
    def update(self, dt, keys):
        self.player.Update(keys, dt)

    #draw
    def on_draw(self):
        self.clear()
        self.player.image_selected.draw()


def main():
    screen = Game(SCREENWIDTH, SCREENHEIGHT, "Game") #parameters: width, hight, title
    screen.set_vsync(True)

    keys = key.KeyStateHandler()
    screen.push_handlers(keys)

    pyglet.clock.schedule_interval(screen.update, screen.frame_rate, keys)
    pyglet.app.run()

    return 0

main()