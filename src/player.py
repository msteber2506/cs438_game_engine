from render import Drawable
from pynput.keyboard import Key


class Player(Drawable):

    def __init__(self, width, height, xloc, yloc):
        super().__init__(width, height, xloc, yloc)

    # def translate(self, dx, dy):
#         translation_matrix = np.array([[1, 0, dx],
#                                        [0, 1, dy],
#                                        [0, 0, 1]])
#         self.position = np.dot(translation_matrix, np.append(self.position, 1))[:2]

#     def rotate(self, angle_degrees):
#         angle_radians = np.radians(angle_degrees)
#         rotation_matrix = np.array([[np.cos(angle_radians), -np.sin(angle_radians), 0],
#                                     [np.sin(angle_radians), np.cos(angle_radians), 0],
#                                     [0, 0, 1]])
#         self.rotation += angle_degrees
#         self.position = np.dot(rotation_matrix, np.append(self.position, 1))[:2]

#     def scale(self, scale_factor):
#         scale_matrix = np.array([[scale_factor, 0, 0],
#                                  [0, scale_factor, 0],
#                                  [0, 0, 1]])
#         self.size *= scale_factor
#         self.position = np.dot(scale_matrix, np.append(self.position, 1))[:2]


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
