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

# class Player:
#     def __init__(self, filepath, frame, resize_factor=0.04):
#         self.sprite = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
#         self.sprite = cv2.resize(self.sprite, (0, 0), fx=resize_factor, fy=resize_factor)
#         self.xloc = 100
#         self.yloc = 100
#         self.speed = 10
#         self.frame = frame

#     def action(self, key):
#         if key == ord('w') and self.yloc > 0:
#             self.yloc -= self.speed
#         elif key == ord('s') and self.yloc < self.frame.background.shape[0] - self.sprite.shape[0]:
#             self.yloc += self.speed
#         elif key == ord('a') and self.xloc > 0:
#             self.xloc -= self.speed
#         elif key == ord('d') and self.xloc < self.frame.background.shape[1] - self.sprite.shape[1]:
#             self.xloc += self.speed


import cv2
import numpy as np

class Player:
    def __init__(self, filepath, frame, resize_factor=0.04):
        self.sprite = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
        self.sprite = self.resize_sprite(self.sprite, resize_factor)
        self.xloc = 100
        self.yloc = 100
        self.speed = 10
        self.frame = frame
        self.resize_factor = resize_factor
        self.original_sprite = self.sprite

    def resize_sprite(self, sprite, resize_factor):
        height, width = sprite.shape[:2]
        new_height = int(height * resize_factor)
        new_width = int(width * resize_factor)

      
        i_indices, j_indices = np.indices((new_height, new_width))

        initial_i_indices = (i_indices / resize_factor).astype(int)
        initial_j_indices = (j_indices / resize_factor).astype(int)


        initial_i_indices = np.clip(initial_i_indices, 0, height - 1)
        initial_j_indices = np.clip(initial_j_indices, 0, width - 1)

        resized_sprite = sprite[initial_i_indices, initial_j_indices]

        return resized_sprite



    

    def rotate_image(self, image, angle_degrees):
        # Convert angle to radians
        angle_radians = np.radians(angle_degrees)

     
        height, width = image.shape[:2]

   
        center_x = width / 2
        center_y = height / 2

    
        cos_theta = np.cos(angle_radians)
        sin_theta = np.sin(angle_radians)

 
        rotation_matrix = np.array([[cos_theta, -sin_theta, 0],
                                    [sin_theta, cos_theta, 0],
                                    [0, 0, 1]])

    
        rotated_image = np.zeros_like(image)


        for y in range(height):
            for x in range(width):
            
                new_x, new_y, _ = np.dot(rotation_matrix, [x - center_x, y - center_y, 1]) + [center_x, center_y, 0]

              
                if 0 <= new_x < width - 1 and 0 <= new_y < height - 1:
                
                    x0, y0 = int(new_x), int(new_y)
                    dx, dy = new_x - x0, new_y - y0

               
                    top_left = image[y0, x0] * (1 - dx) * (1 - dy)
                    top_right = image[y0, x0 + 1] * dx * (1 - dy)
                    bottom_left = image[y0 + 1, x0] * (1 - dx) * dy
                    bottom_right = image[y0 + 1, x0 + 1] * dx * dy

            
                    rotated_image[y, x] = top_left + top_right + bottom_left + bottom_right

        return rotated_image
    
    def shear_image(image, shear_x=-0.9, shear_y=0.1):
        image = np.array(image)

        #shear_matrix = np.array([[1, shear_x, 0],[shear_y, 1, 0]])


        output_height = int(image.shape[0] + abs(shear_y) * image.shape[1])
        output_width = int(image.shape[1] + abs(shear_x) * image.shape[0])

    
        sheared_image = np.zeros((output_height, output_width, image.shape[2]), dtype=np.uint8)


        for y in range(output_height):
            for x in range(output_width):
            
                new_sheared_x = int(x + shear_x * (y - output_height / 2))
                new_sheared_y = int(y + shear_y * (x - output_width / 2))

                
                if 0 <= new_sheared_x < image.shape[1] and 0 <= new_sheared_y < image.shape[0]:
                
                    sheared_image[y, x] = image[new_sheared_y, new_sheared_x]

        return sheared_image
    




    def action(self, key):
        if key == ord('w') and self.yloc > 0:
            self.yloc -= self.speed
        elif key == ord('s') and self.yloc < self.frame.background.shape[0] - self.sprite.shape[0]:
            self.yloc += self.speed
        elif key == ord('a') and self.xloc > 0:
            self.xloc -= self.speed
        elif key == ord('d') and self.xloc < self.frame.background.shape[1] - self.sprite.shape[1]:
            self.xloc += self.speed
        elif key == ord('r'):
            #self.resize_factor += 0.01  
            self.resize_factor = 0.7 
            self.sprite = self.resize_sprite(self.sprite, self.resize_factor)
        elif key == ord('t'):
            #self.resize_factor -= 0.01  
            self.resize_factor = 1.3
            if self.resize_factor <= 0:
                self.resize_factor = 0.01  
            self.sprite = self.resize_sprite(self.sprite, self.resize_factor)
        elif key == ord('i'):
            
            self.sprite = self.rotate_image(self.sprite, 90)
        elif key == ord('o'):
            self.sprite = self.original_sprite
    
            






