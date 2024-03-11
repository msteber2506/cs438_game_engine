import stat
from turtle import st
import cv2
import numpy as np
from pathlib import Path
import constants
import textwrap
from PIL import Image, ImageDraw, ImageFont
import pickle

class RenderingEngine:
    def __init__(self):
        pass

    @staticmethod
    def find_image_files(directory):
        #assumes you name your files 0.png, 1.png, 3.png, etc.
        dir_path = Path(directory)

        image_files = dir_path.glob('**/*.png')
        image_files_sorted = sorted(image_files, key=lambda x: int(x.stem))

        image_paths = [str(file.resolve()) for file in image_files_sorted]
        #print(image_paths)
        return image_paths
    
    @staticmethod
    def load_images(image_paths):
        image_list = []
        for path in image_paths:
            image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if image is not None:
                image_list.append(image)
        return image_list
    
    @staticmethod
    def render_to_screen(name, scene, shape):
        cv2.imshow(name, scene)
        height, width = shape
        cv2.resizeWindow(name, width, height)

    @staticmethod
    def overlay_image(bg, fg, coordinates, alpha=1.0):
        x, y = coordinates
        if bg.shape[2] == 3:
            bg = cv2.cvtColor(bg, cv2.COLOR_BGR2BGRA)
        if fg.shape[2] == 3:
            fg = cv2.cvtColor(fg, cv2.COLOR_BGR2BGRA)

        bh,bw = bg.shape[:2]
        fh,fw = fg.shape[:2]
        x1, x2 = max(x, 0), min(x+fw, bw)
        y1, y2 = max(y, 0), min(y+fh, bh)

        
        fg_cropped = fg[y1-y:y2-y, x1-x:x2-x]
        bg_cropped = bg[y1:y2, x1:x2]

        alpha_fg = fg_cropped[:,:,3:4] / 255 * alpha
        alpha_bg = bg_cropped[:,:,3:4] / 255

        
        
        result = bg.copy()

        result[y1:y2, x1:x2, :3] = alpha_fg * fg_cropped[:,:,:3] + (1-alpha_fg) * bg_cropped[:,:,:3]
        result[y1:y2, x1:x2, 3:4] = (alpha_fg + alpha_bg) / (1 + alpha_fg*alpha_bg) * 255

        return result
    
    @staticmethod
    def create_background(image_path_to_coordinates_dict):
        
        image_path_list, coordinates_list = list(image_path_to_coordinates_dict.keys()), list(image_path_to_coordinates_dict.values())
        #new_window = window.copy()
        image_list = []
        
        for index, path in enumerate(image_path_list):
            image = cv2.imread(path, cv2.IMREAD_UNCHANGED)

            if image.shape[2] != 4: 
                image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

            image_list.append(image)
        
        for index, image in enumerate(image_list):
            if index != 0:
                image_list[0] = RenderingEngine.overlay_image(image_list[0], image, coordinates_list[index])
            #new_window = SceneManager.overlay_image(new_window, image, coordinates_list[index])
           

        #new_window = cv2.resize(new_window, (constants.TILE_MAP_SCREEN_WIDTH, constants.TILE_MAP_SCREEN_HEIGHT))
        image_list[0] = cv2.resize(image_list[0], (constants.TILE_MAP_SCREEN_WIDTH, constants.TILE_MAP_SCREEN_HEIGHT))
        return image_list[0]
    
    @staticmethod
    def create_full_background(background_img, new_width):
        #sample the background to achieve user-specified map width
        #print(f"background img shape: {background_img.shape}")
        old_height, old_width, _ = background_img.shape
        #print(f"old_height = {old_height}")
        #print(f"n")
        new_image = np.zeros((old_height, new_width, 4), dtype=np.uint8)
        #print(f"new_image: {new_image.shape}")
        num_repetitions = int(np.ceil(new_width / old_width))
        #print(f"num reps: {num_repetitions}")
     
        for i in range(num_repetitions):
            start_x = i * old_width
            end_x = min(start_x + old_width, new_width)
            new_image[:, start_x:end_x] = background_img[:, :end_x - start_x]

        #print(f"new_image: {new_image.shape}")
        return new_image
    
    @staticmethod
    def render_text_on_image(image, text, font_path, font_size=38, text_color=(255, 255, 255), opacity=255, position=(10, 10), width=20):
      
        pil_image = Image.fromarray(image)


        wrapped_text = textwrap.wrap(text, width=width)

  
        wrapped_text_str = '\n'.join(wrapped_text)

     
        font = ImageFont.truetype(font_path, size=font_size)

 
        draw = ImageDraw.Draw(pil_image)

        text_color_with_opacity = text_color[:3] + (opacity,)

        draw.text(position, wrapped_text_str, fill=text_color_with_opacity, font=font)

        cv_image = np.array(pil_image)

        return cv_image
    
    @staticmethod
    def load_pickled_data(file_path):
        try:
            with open(file_path, 'rb') as file:
                unpickled_data = pickle.load(file)
            return unpickled_data
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"Error occurred while loading pickled data: {e}")
            return None
        
    @staticmethod
    def draw_world(full_bg, map_data, tile_list):
        cur_window = full_bg.copy()
        for row_num, row in enumerate(map_data):
            for col_num, tile in enumerate(row):
                if tile >= 0:
                    x_coor = col_num * constants.TILE_SIZE
                    y_coor = row_num * constants.TILE_SIZE
                    cur_window = RenderingEngine.overlay_image(cur_window, tile_list[tile], (x_coor, y_coor))

        return cur_window
    
    @staticmethod     
    def scroll(full_image, virtual_window_position, window_width):
        # Calculate the end position of the virtual window
        window_end = virtual_window_position + window_width
        
        # Extract the portion of the full image within the virtual window
        scrolled_image = full_image[:, virtual_window_position:window_end].copy()
        
        return scrolled_image
    
    @staticmethod
    def construct_scene(window,full_bg, map_data, tile_list, virtual_window_position):
    
        new_scene = RenderingEngine.draw_world(full_bg, map_data, tile_list)
    
        new_scene = RenderingEngine.scroll(new_scene, virtual_window_position, constants.WINDOW_WIDTH)


        new_scene = RenderingEngine.overlay_image(window, new_scene, (0,0))
        return new_scene
        #RenderingEngine.render_to_screen(constants.WINDOW_NAME, new_scene, (constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))
        
        

        

    @staticmethod
    def scroll_render(window,full_bg, map_data, tile_list, virtual_window_position, isScrollToRight, sprite):
        if isScrollToRight:
            if virtual_window_position + constants.SCROLL_AMOUNT <= full_bg.shape[1] - constants.WINDOW_WIDTH:
                virtual_window_position += constants.SCROLL_AMOUNT

                new_scene = RenderingEngine.construct_scene(window,full_bg, map_data, tile_list, virtual_window_position)
                new_scene = RenderingEngine.overlay_image(new_scene, sprite.sprite_images[sprite.current_frame], (sprite.xloc, sprite.yloc))
                RenderingEngine.render_to_screen(constants.WINDOW_NAME, new_scene, (constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))

                
        else:
            if virtual_window_position - constants.SCROLL_AMOUNT >= 0:
                virtual_window_position -= constants.SCROLL_AMOUNT

                RenderingEngine.construct_scene(window,full_bg, map_data, tile_list, virtual_window_position)
               
        return virtual_window_position
                

    @staticmethod
    def bresenham_line(start_coordinates, end_coordinates):
        x0, y0 = start_coordinates
        x1, y1 = end_coordinates

        step_size_x, step_size_y = abs(x1 - x0), abs(y1 - y0)
        move_to_the_right = 1
        move_to_the_left = -1
        move_downward = 1
        move_upward = -1

        direction_x = move_to_the_right if x0 < x1 else move_to_the_left
        direction_y = move_downward if y0 < y1 else move_upward
        error = step_size_x - step_size_y

        line = []
        while True:
            line.append((x0, y0))

            if x0 == x1 and y0 == y1:
                break
            
            accumulated_error = 2 * error
            if accumulated_error > -step_size_y:
                error -= step_size_y
                x0 += direction_x
            if accumulated_error < step_size_x:
                error += step_size_x
                y0 += direction_y

        return np.array(line)
    



class ImageProcessor:
    def __init__(self):
        pass

    @staticmethod
    def downscaling(image, new_height, new_width):
        #Uses bilineaer interpolation for resizing
        if image.shape[2] == 4: 
            image = image[:, :, :3]
        height, width = image.shape[:2]
        scale_y = height / new_height
        scale_x = width / new_width
        
        y_indices, x_indices = np.indices((new_height, new_width), dtype=np.float32)
        
        y_original = y_indices * scale_y
        x_original = x_indices * scale_x
        
        y0 = np.floor(y_original).astype(int)
        y1 = np.minimum(y0 + 1, height - 1)
        x0 = np.floor(x_original).astype(int)
        x1 = np.minimum(x0 + 1, width - 1)
        
        dy = y_original - y0
        dx = x_original - x0
        dy_inv = 1 - dy
        dx_inv = 1 - dx
        

        dy = np.expand_dims(dy, axis=2)
        dx = np.expand_dims(dx, axis=2)
        
        
        dx_inv = np.tile(dx_inv[:, :, np.newaxis], (1, 1, 3))
        dy_inv = np.tile(dy_inv[:, :, np.newaxis], (1, 1, 3))
        # dx_inv = np.tile(dx_inv[:, :, np.newaxis], (1, 1, 4))
        # dy_inv = np.tile(dy_inv[:, :, np.newaxis], (1, 1, 4))

        print("image[y0, x0].shape",image[y0, x0].shape)
        print("dx_inv.shape",dx_inv.shape)
        print("dx.shape",dx.shape)
        interpolated_values = (image[y0, x0] * dx_inv * dy_inv +
                            image[y0, x1] * dx * dy_inv +
                            image[y1, x0] * dx_inv * dy +
                            image[y1, x1] * dx * dy)
        
        return interpolated_values.astype(np.uint8)
    
    @staticmethod
    def upscaling(image, new_height, new_width):
        if image.shape[2] == 4: 
            image = image[:, :, :3]
        #Uses bilineaer interpolation for resizing
        height, width = image.shape[:2]
        scale_y = new_height / height
        scale_x = new_width / width
        
      
        y_indices, x_indices = np.indices((new_height, new_width), dtype=np.float32)
        
    
        y_original = y_indices / scale_y
        x_original = x_indices / scale_x
        

        y0 = np.floor(y_original).astype(int)
        y1 = np.minimum(y0 + 1, height - 1)
        x0 = np.floor(x_original).astype(int)
        x1 = np.minimum(x0 + 1, width - 1)
        
       
        dx = x_original - x0
        dy = y_original - y0
        # print(f"dy before size = {dy.shape}")
        # print(f"dx before size = {dx.shape}")

        #broadcast to new dimensions
        dx = dx[:, :, np.newaxis]
        dy = dy[:, :, np.newaxis]

        

        dx_inv = 1 - dx
        dy_inv = 1 - dy
        # print(f"dx_inv before size = {dx_inv.shape}")
        # print(f"dy_inv  before size = {dy_inv.shape}")

        #broadcast to new dimension
        # dx_inv = dx_inv[:, :, np.newaxis]
        # dy_inv = dy_inv[:, :, np.newaxis]

        # Reshape dx_inv and dy_inv
        dx_inv = np.tile(dx_inv, (1, 1, 3))
        dy_inv = np.tile(dy_inv, (1, 1, 3))
        
        # print(f"original image shape = {image.shape}")
        # print(f"scale_x = {scale_x}")
        # print(f"scale_y = {scale_y}")
        # print(f"x_indices shape: {x_indices.shape}")
        # print(f"y_indices shape = {y_indices.shape}")
        # print(f"y0 size = {y0.shape}")
        # print(f"y1 size = {y1.shape}")
        # print(f"x0 size = {x0.shape}")
        # print(f"x1 size = {x1.shape}")
        # print(f"dx size = {dx.shape}")
        # print(f"dy size = {dy.shape}")
        # print(f"dx_inv size = {dx_inv.shape}")
        # print(f"dy_inv size = {dy_inv.shape}")
        # print(f"image[y0, x0] = {image[y0, x0].shape}")
        # print(f"image[y0, x1] = {image[y0, x1].shape}")
        # print(f"image[y1, x0] = {image[y1, x0].shape}")
        # print(f"image[y1, x1] = {image[y1, x1].shape}")
        # Perform bilinear interpolation
        interpolated_values = (image[y0, x0] * dx_inv * dy_inv +
                            image[y0, x1] * dx * dy_inv +
                            image[y1, x0] * dx_inv * dy +
                            image[y1, x1] * dx * dy)
        
        return interpolated_values.astype(np.uint8)


    
    

    @staticmethod
    def flip_image_y_axis(image):
        # Check if the image is valid
        if image is None:
            print("Error: Input image is invalid.")
            return None

        # Get the dimensions of the image
        height, width, _ = image.shape

        # Create an empty array to store the flipped image
        flipped_image = np.empty_like(image)

        # Flip the image along the y-axis by reversing the order of columns in each row
        for row in range(height):
            flipped_image[row, :] = image[row, ::-1]

        return flipped_image
    
    @staticmethod
    def rotate(image, angle):
        height, width = image.shape[:2]
        center = (width / 2, height / 2)

      
        angle_rad = np.deg2rad(angle)

  
        rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                    [np.sin(angle_rad), np.cos(angle_rad)]])


        new_width = int(np.ceil(width * np.abs(np.cos(angle_rad)) + height * np.abs(np.sin(angle_rad))))
        new_height = int(np.ceil(width * np.abs(np.sin(angle_rad)) + height * np.abs(np.cos(angle_rad))))


        tx = (new_width - width) / 2
        ty = (new_height - height) / 2

        rotated_image = np.zeros((new_height, new_width, 3), dtype=np.uint8)

        for y in range(new_height):
            for x in range(new_width):
        
                x_centered = x - center[0] - tx
                y_centered = y - center[1] - ty

          
                x_rotated, y_rotated = np.dot(rotation_matrix, [x_centered, y_centered])

                x_rotated += center[0]
                y_rotated += center[1]


                x_floor, y_floor = int(np.floor(x_rotated)), int(np.floor(y_rotated))
                x_ceil, y_ceil = x_floor + 1, y_floor + 1

                if 0 <= x_floor < width - 1 and 0 <= x_ceil < width and 0 <= y_floor < height - 1 and 0 <= y_ceil < height:
                    x_weight = x_rotated - x_floor
                    y_weight = y_rotated - y_floor

                    top_left = image[y_floor, x_floor] * (1 - x_weight) * (1 - y_weight)
                    top_right = image[y_floor, x_ceil] * x_weight * (1 - y_weight)
                    bottom_left = image[y_ceil, x_floor] * (1 - x_weight) * y_weight
                    bottom_right = image[y_ceil, x_ceil] * x_weight * y_weight

                    rotated_image[y, x] = np.clip(top_left + top_right + bottom_left + bottom_right, 0, 255).astype(np.uint8)

        return rotated_image
    
    @staticmethod
    def render_motion_blur(trailing_sprites, window):
        scene = window.copy()
        for sprite_info in trailing_sprites:
            # Extract sprite_x, sprite_y, and alpha values from sprite_info
            sprite_x, sprite_y, alpha = sprite_info
            
            # Render the sprite on the scene
            scene = overlay_image(scene, sprite, sprite_x, sprite_y, alpha)
        return scene
    @staticmethod
    def update_trailing_sprites(coordinates, velocity, num_trailing_sprites, alpha_initial, key):
        sprite_x, sprite_y = coordinates
        # Generate alpha values using np.linspace()
        alpha_values = np.linspace(alpha_initial, 1.0, num_trailing_sprites) 

        if key == "w":
            sprites = [(sprite_x, sprite_y +  (i * velocity), alpha_values[len(alpha_values) - 1 - i]) for i in range(num_trailing_sprites)]
            sprites = list(reversed(sprites))
        elif key == "s":
            sprites = [(sprite_x, sprite_y +  (i * velocity), alpha_values[i]) for i in range(num_trailing_sprites)]
        elif key == "a":
            sprites = [(sprite_x + (i * velocity), sprite_y, alpha_values[len(alpha_values) - 1 - i]) for i in range(num_trailing_sprites)]
            sprites = list(reversed(sprites))
            
        elif key == "d":
            sprites = [(sprite_x + (i * velocity), sprite_y, alpha_values[i]) for i in range(num_trailing_sprites)]

        
        return sprites
    


class Sprite:
    def __init__(self, image_paths, coordinates):
        self.sprite_images = [cv2.imread(image_path, cv2.IMREAD_UNCHANGED) for image_path in image_paths]
        self.current_frame = 0
        self.xloc = coordinates[0]
        self.yloc = coordinates[1]
        self.speed = 10

    # def move(self, direction):
    #     # Update sprite location based on direction
    #     if direction == "right":
    #         self.xloc += self.speed
    #         self.current_frame = (self.current_frame + 1) % len(self.sprite_images)

            
    #     elif direction == "left":
    #         self.xloc -= self.speed
    #         self.current_frame = (self.current_frame + 1) % len(self.sprite_images)
        
    def move(self, direction, window, full_bg, map_data, tile_list, virtual_window_position, clean_map):
        # Update sprite location based on direction
        virtual_window_position
        if direction == "right":
            if self.xloc + self.speed + self.sprite_images[self.current_frame].shape[1] >= constants.WINDOW_WIDTH:
                virtual_window_position = RenderingEngine.scroll_render(window, full_bg, map_data, tile_list, virtual_window_position, isScrollToRight=True, sprite=self)

                print(f"virtual = {virtual_window_position}")
                # scene = RenderingEngine.overlay_image(clean_map, self.sprite_images[self.current_frame], (self.xloc, self.yloc))
                # RenderingEngine.render_to_screen(constants.WINDOW_NAME, scene, (constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))
            else:
                self.xloc += self.speed
                self.current_frame = (self.current_frame + 1) % len(self.sprite_images)
                scene = RenderingEngine.overlay_image(clean_map, self.sprite_images[self.current_frame], (self.xloc, self.yloc))
                RenderingEngine.render_to_screen(constants.WINDOW_NAME, scene, (constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))
        elif direction == "left":
            if self.xloc - self.speed <= 0:
                virtual_window_position = RenderingEngine.scroll_render(window, full_bg, map_data, tile_list, virtual_window_position, isScrollToRight=False, sprite=self)
                scene = RenderingEngine.overlay_image(clean_map, ImageProcessor.flip_image_y_axis(self.sprite_images[self.current_frame]), (self.xloc, self.yloc))
                RenderingEngine.render_to_screen(constants.WINDOW_NAME, scene, (constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))
            else:
                self.xloc -= self.speed
                self.current_frame = (self.current_frame + 1) % len(self.sprite_images)
                scene = RenderingEngine.overlay_image(clean_map, ImageProcessor.flip_image_y_axis(self.sprite_images[self.current_frame]), (self.xloc, self.yloc))
                RenderingEngine.render_to_screen(constants.WINDOW_NAME, scene, (constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))
        return virtual_window_position
 




    
