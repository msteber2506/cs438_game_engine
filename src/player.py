import cv2
from render import Drawable
from pynput.keyboard import Key
from physics import Collision

class Player(Drawable):

    def __init__(self, width, height, xloc, yloc, sprite=None, speed=5):
        super().__init__(width, height, xloc, yloc)
        if sprite is not None:
            im = cv2.imread(sprite)
            self.sprite = cv2.resize(im, (width, height))
        self.speed = speed

    def draw(self, frame):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if y+self.yloc < frame.height and x+self.xloc < frame.width:
                    if self.sprite is not None:
                        frame.frame[y+self.yloc, x+self.xloc] = self.sprite[y, x]
                    else:
                        frame.frame[y+self.yloc, x+self.xloc] = [255, 0, 0]

#     def translate(self, dx, dy):
#         translation_matrix = np.array([[1, 0, dx],
#                                        [0, 1, dy],
#                                        [0, 0, 1]])
#
#     def rotate(self, angle_degrees):
#         angle_radians = np.radians(angle_degrees)
#         rotation_matrix = np.array([[np.cos(angle_radians), -np.sin(angle_radians), 0],
#                                     [np.sin(angle_radians), np.cos(angle_radians), 0],
#                                     [0, 0, 1]])
#         

#     def scale(self, scale_factor):
#         scale_matrix = np.array([[scale_factor, 0, 0],
#                                  [0, scale_factor, 0],
#                                  [0, 0, 1]])

    #move player around the screen
    def action(self, key):
        if key == Key.up:
            self.move("up")
        if key == Key.down:
            self.move("down")
        if key == Key.left:
            self.move("left")
        if key == Key.right:
            self.move("right")

    def move(self, direction):
        if direction == "up":
            self.yloc -= self.speed
        if direction == "down":
            self.yloc += self.speed
        if direction == "left":
            self.xloc -= self.speed
        if direction == "right":
            self.xloc += self.speed
