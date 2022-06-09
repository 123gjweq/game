import pyglet
from player import Player
from pyglet.window import key
from vector2 import Vector2

# player = Player()

# while gameRunnng:
    # events
    # Update
    # Draw

class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        self.frame_rate = 1/60.0

        #player stuff
        self.player = Player(Vector2(0, 0))
        self.player_sprite = pyglet.sprite.Sprite(self.player.imageSelected, x=0, y=0)


    #events
    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, buttom, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass




    #update
    def update(self, dt, keys):
        self.player.Update(keys, "leftclicking", dt)
        self.player_sprite.x, self.player_sprite.y = self.player.pos.x, self.player.pos.y



    #draw
    def on_draw(self):
        self.clear()
        self.player_sprite.draw()



def main():
    screen = Game(1500, 900, "Game") #parameters: width, hight, title of program
    screen.set_vsync(True) #look up vsync for more info

    keys = key.KeyStateHandler()
    screen.push_handlers(keys)

    pyglet.clock.schedule_interval(screen.update, screen.frame_rate, keys)
    pyglet.app.run()
    return 1

main()