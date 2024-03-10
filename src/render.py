import numpy as np
import cv2


class Drawable:

    def __init__(self, width, height, xloc, yloc, rigidbody=None):
        self.width = width
        self.height = height
        self.xloc = xloc
        self.yloc = yloc
        self.rigidbody = rigidbody

    def draw(self, frame):
        if self.rigidbody:
            # Update position of the drawable
            self.xloc = int(self.rigidbody.position.x)
            self.yloc = int(self.rigidbody.position.y)

        for y in range(0, self.height):
            for x in range(0, self.width):
                if y+self.yloc < frame.height and x+self.xloc < frame.width:
                    frame.frame[y+self.yloc, x+self.xloc] = [255, 0, 0]


class Frame:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.frame = np.zeros((width, height, 3), dtype=np.uint8)
        self.drawables = []
        cv2.namedWindow('Game Screen', cv2.WINDOW_NORMAL)

    def render(self):
        cv2.imshow('Game Screen', self.frame)

    def update(self):
        self.frame = np.zeros((self.width, self.height, 3), dtype=np.uint8)
        for drawable in self.drawables:
            drawable.draw(self)

    def add_drawable(self, drawable):
        self.drawables.append(drawable)
    
    # def check_collisions(self):
    #     for i, drawable1 in enumerate(self.drawables):
    #         for j, drawable2 in enumerate(self.drawables):
    #             if i != j:  # Don't check collision with itself
    #                 if Collision.intersect(drawable1, drawable2):
    #                     # Handle collision between drawables
    #                     pass








