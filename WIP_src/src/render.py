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

#     def add_drawable(self, drawable):
#         self.drawables.append(drawable)
class Frame:
    def __init__(self, filepath):
        self.background = cv2.imread(filepath)
        self.background_x = 0
        self.frame = np.zeros_like(self.background)
        self.start_x = self.background_x % self.background.shape[1]
        self.sprite_width = 0
        self.sprite_height = 0


    def render_with_physics(self, physics_objects):
        # Render background
        self.frame = np.zeros_like(self.background)
        self.start_x = self.background_x % self.background.shape[1]
        self.frame[:, self.start_x:] = self.background[:, :self.background.shape[1] - self.start_x]
        self.frame[:, :self.start_x] = self.background[:, self.background.shape[1] - self.start_x:]

        # Render physics objects
        for obj in physics_objects:
            self.render(obj)

        # Show frame
        cv2.imshow('Game', self.frame)

    def render(self, obj):
        # Render the object onto the frame
        sprite = obj.sprite
        sprite_height, sprite_width = sprite.shape[:2]
        region_height = min(sprite_height, self.frame.shape[0] - obj.yloc)
        region_width = min(sprite_width, self.frame.shape[1] - obj.xloc)

        alpha_channel = sprite[:, :, 3] / 255.0
        for c in range(3): 
            self.frame[obj.yloc:obj.yloc + region_height, obj.xloc:obj.xloc + region_width, c] = \
                (1.0 - alpha_channel[:region_height, :region_width]) * self.frame[obj.yloc:obj.yloc + region_height, obj.xloc:obj.xloc + region_width, c] + \
                alpha_channel[:region_height, :region_width] * sprite[:region_height, :region_width, c]
        
    def move_background(self, sprite):
        if sprite.xloc <= 0:
            self.background_x += sprite.speed
        elif sprite.xloc >= self.background.shape[1] - self.sprite_width:
            self.background_x -= sprite.speed


class Game:

    def __init__(self, frame, physics_world):
        self.frame = frame
        self.physics_world = physics_world

    @staticmethod
    def tick(self, fps):
        interval = 1.0 / fps
        self.update_physics(interval)
        self.frame.render_with_physics(self.physics_world.objects)
        time.sleep(interval)






