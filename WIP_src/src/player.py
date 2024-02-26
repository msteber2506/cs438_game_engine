from render import Drawable
from pynput.keyboard import Key
import cv2


# class Player(Drawable):

#     def __init__(self, width, height, xloc, yloc):
#         super().__init__(width, height, xloc, yloc)


#     #move player around the screen
#     def action(self, key):
#         if key == Key.up:
#             self.yloc -= 5
#         if key == Key.down:
#             self.yloc += 5
#         if key == Key.left:
#             self.xloc -= 5
#         if key == Key.right:
#             self.xloc += 5

class Player:
    def __init__(self, filepath, frame, resize_factor=0.08):
        self.sprite = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
        self.sprite = cv2.resize(self.sprite, (0, 0), fx=resize_factor, fy=resize_factor)
        self.xloc = 100
        self.yloc = 100
        self.speed = 10
        self.frame = frame

    def move(self, key):
        if key == ord('w') and self.yloc > 0:
            self.yloc -= self.speed
        elif key == ord('s') and self.yloc < self.frame.background.shape[0] - self.sprite.shape[0]:
            self.yloc += self.speed
        elif key == ord('a') and self.xloc > 0:
            self.xloc -= self.speed
        elif key == ord('d') and self.xloc < self.frame.background.shape[1] - self.sprite.shape[1]:
            self.xloc += self.speed
