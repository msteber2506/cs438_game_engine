import numpy as np
import cv2
import time


class Drawable:

    def __init__(self, width, height, xloc, yloc):
        self.width = width
        self.height = height
        self.xloc = xloc
        self.yloc = yloc

    def draw(self, frame):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if y+self.yloc < frame.height and x+self.xloc < frame.width:
                    frame.frame[y+self.yloc, x+self.xloc] = [255, 0, 0, 50]


class Frame:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.frame = np.zeros((width, height, 4), dtype=np.uint8)
        self.drawables = []
        cv2.namedWindow('Game Screen', cv2.WINDOW_NORMAL)

    def render(self):
        cv2.imshow('Game Screen', self.frame)

    def update(self):
        self.frame = np.zeros((self.width, self.height, 4), dtype=np.uint8)
        for drawable in self.drawables:
            drawable.draw(self)

    def addDrawable(self, drawable):
        self.drawables.append(drawable)


class Game:

    def __init__(self, frame):
        self.frame = frame

    @staticmethod
    def tick(fps):
        interval = 1.0 / fps
        time.sleep(interval)


if __name__ == '__main__':

    frame = Frame(500, 500)
    game = Game(frame)

    square = Drawable(50,50, 0, 0)
    frame.addDrawable(square)

    while True:
        # main game loop code goes here
        square.xloc += 1
        square.yloc += 1

        # update and render frame
        frame.update()
        frame.render()
        Game.tick(30)
        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break
    cv2.destroyAllWindows()



