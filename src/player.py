from render import Drawable
from pynput.keyboard import Key


class Player(Drawable):

    def __init__(self, width, height, xloc, yloc):
        super().__init__(width, height, xloc, yloc)




    #move player around the screen
    def action(self, key):
        if key == Key.up:
            self.yloc -= 5
        if key == Key.down:
            self.yloc += 5
        if key == Key.left:
            self.xloc -= 5
        if key == Key.right:
            self.xloc += 5
