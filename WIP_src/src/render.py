import numpy as np
import cv2
import time


class Drawable:

    def __init__(self, width, height, xloc, yloc):
        self.width = width
        self.height = height
        self.xloc = xloc
        self.yloc = yloc

    # def draw(self, frame):
    #     for y in range(0, self.height):
    #         for x in range(0, self.width):
    #             if y+self.yloc < frame.height and x+self.xloc < frame.width:
    #                 frame.frame[y+self.yloc, x+self.xloc] = [255, 0, 0, 50]
    def draw(self, frame):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if y+self.yloc < frame.height and x+self.xloc < frame.width:
                    frame.frame[y+self.yloc, x+self.xloc] = self.sprite[y, x]  # Assign pixel value from the PNG image

        

#simulate the frame buffer
# class Frame:

#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
#         self.frame = np.zeros((width, height, 4), dtype=np.uint8)
#         self.drawables = []
#         cv2.namedWindow('Game Screen', cv2.WINDOW_NORMAL)

#     def render(self):
#         cv2.imshow('Game Screen', self.frame)

#     def update(self):
#         self.frame = np.zeros((self.width, self.height, 4), dtype=np.uint8)
#         for drawable in self.drawables:
#             drawable.draw(self)

#     def addDrawable(self, drawable):
#         self.drawables.append(drawable)
class Frame:
    def __init__(self, filepath):
        self.background = cv2.imread(filepath)
        self.background_x = 0
        self.frame = np.zeros_like(self.background)
        self.start_x = self.background_x % self.background.shape[1]
        self.sprite_width = 0
        self.sprite_height = 0


    def render(self, sprite):
        self.frame = np.zeros_like(self.background)
        self.start_x = self.background_x % self.background.shape[1]
        self.frame[:, self.start_x:] = self.background[:, :self.background.shape[1] - self.start_x]
        self.frame[:, :self.start_x] = self.background[:, self.background.shape[1] - self.start_x:]

        self.sprite_height, self.sprite_width = sprite.sprite.shape[:2]
        region_height, region_width = min(self.sprite_height, self.frame.shape[0] - sprite.yloc), min(self.sprite_width, self.frame.shape[1] - sprite.xloc)
        alpha_channel = sprite.sprite[:, :, 3] / 255.0
        for c in range(3): 
            self.frame[sprite.yloc:sprite.yloc + region_height, sprite.xloc:sprite.xloc + region_width, c] = \
                (1.0 - alpha_channel[:region_height, :region_width]) * self.frame[sprite.yloc:sprite.yloc + region_height, sprite.xloc:sprite.xloc + region_width, c] + \
                alpha_channel[:region_height, :region_width] * sprite.sprite[:region_height, :region_width, c]
        
        cv2.imshow('Game', self.frame)
        
    def move_background(self, sprite):
        if sprite.xloc <= 0:
            self.background_x += sprite.speed
        elif sprite.xloc >= self.background.shape[1] - self.sprite_width:
            self.background_x -= sprite.speed


class Game:

    def __init__(self, frame):
        self.frame = frame

    @staticmethod
    def tick(fps):
        interval = 1.0 / fps
        time.sleep(interval)






