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
    def scroll(full_image, virtual_window_position, window_width, scroll_amount):
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

    
        
        RenderingEngine.render_to_screen(constants.WINDOW_NAME, new_scene, (constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))

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
        

        dy = np.expand_dims(dy, axis=-1)
        dx = np.expand_dims(dx, axis=-1)
        
        dx_inv = np.tile(dx_inv[:, :, np.newaxis], (1, 1, 3))
        dy_inv = np.tile(dy_inv[:, :, np.newaxis], (1, 1, 3))
        
        interpolated_values = (image[y0, x0] * dx_inv * dy_inv +
                            image[y0, x1] * dx * dy_inv +
                            image[y1, x0] * dx_inv * dy +
                            image[y1, x1] * dx * dy)
        
        return interpolated_values.astype(np.uint8)
    
    @staticmethod
    def upscaling(image, new_height, new_width):
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