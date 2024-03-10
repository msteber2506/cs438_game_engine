import numpy as np
import cv2
import constants
from pathlib import Path



class SceneManager:
    def __init__(self):
        pass

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
    def render(name, scene, shape):
        cv2.imshow(name, scene)

        height, width = shape
        cv2.resizeWindow(name, width, height)
    
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
                image_list[0] = SceneManager.overlay_image(image_list[0], image, coordinates_list[index])
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
    def draw_line(image, start_coordinates, end_coordinates, type, color=(0,0,0)):
        start_x, start_y = start_coordinates
        end_x, end_y = end_coordinates
        line_color = np.array(color + (255,)).reshape(1, 1, -1)
        if type == "vertical":
       

            line_color = np.tile(line_color, (end_y - start_y, 1, 1))

            image[start_y:end_y, start_x:start_x+1, :] = line_color
        elif type == "horizontal": 
            
            line_color = np.tile(line_color, (1, end_x - start_x, 1))
            
            
            image[start_y:start_y+1, start_x:end_x, :] = line_color

        return image
    
    @staticmethod
    def draw_grid(image, color):
        
        for i in range(constants.TILE_MAP_SCREEN_WIDTH // constants.TILE_SIZE):
            #x_coor = i * tile_size  
            x_coor = i * constants.TILE_SIZE  
            image = SceneManager.draw_line(image, (x_coor, 0), (x_coor, constants.TILE_MAP_SCREEN_HEIGHT), "vertical", color)

        for i in range(constants.TILE_MAP_SCREEN_HEIGHT // constants.TILE_SIZE):
            #y_coor = i * tile_size
            y_coor = i * constants.TILE_SIZE  
            image = SceneManager.draw_line(image, (0, y_coor), (constants.TILE_MAP_SCREEN_WIDTH, y_coor), "horizontal", color)
            
        return image
    
    
    @staticmethod
    def draw_world(full_bg, map_data, tile_list):
        cur_window = full_bg.copy()
        for row_num, row in enumerate(map_data):
            for col_num, tile in enumerate(row):
                if tile >= 0:
                    x_coor = col_num * constants.TILE_SIZE
                    y_coor = row_num * constants.TILE_SIZE
                    cur_window = SceneManager.overlay_image(cur_window, tile_list[tile], (x_coor, y_coor))

        return cur_window
    
    @staticmethod
    def find_image_files(directory):
        dir_path = Path(directory)

        image_files = dir_path.glob('**/*.png')
        image_files_sorted = sorted(image_files, key=lambda x: int(x.stem))

        image_paths = [str(file.resolve()) for file in image_files_sorted]
        #print(image_paths)
        return image_paths
                    



