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
        self.client_mouse_pos = Vector2()
        self.is_leftclicking = False

        #player stuff
        self.player = Player(Vector2(0, 0))


    #events
    def on_mouse_motion(self, x, y, dx, dy):
        self.client_mouse_pos.x, self.client_mouse_pos.y = x, y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.client_mouse_pos.x, self.client_mouse_pos.y = x, y

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:
            self.is_leftclicking = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == 1:
            self.is_leftclicking = False

    #update
    def update(self, dt, keys):
        self.player.Update(keys, dt, self.is_leftclicking, self.client_mouse_pos)

    #draw
    def on_draw(self):
        self.clear()
        self.player.image_selected.draw()
        REFERENCEPOINT.blit(self.player.player_camera.x, self.player.player_camera.y)


def main():
    screen = Game(SCREENWIDTH, SCREENHEIGHT, "Game") #parameters: width, hight, title
    screen.set_vsync(True)

    keys = key.KeyStateHandler()
    screen.push_handlers(keys)

    pyglet.clock.schedule_interval(screen.update, screen.frame_rate, keys)
    pyglet.app.run()

    return 0

main()