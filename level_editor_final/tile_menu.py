import numpy as np
import cv2
import constants
import math
from scene_manager import SceneManager
class TileMenu:
    def __init__(self, tile_directory):
        self.tile_list = []
        self.tile_directory = tile_directory
        self.tile_loc = []
        self.tile_menu_organized = []

    def load_tiles(self):
        image_paths = SceneManager.find_image_files(constants.TILE_IMAGE_DIRECTORY)
        # for x in range(constants.TILE_TYPES):

        #     image = cv2.imread(f"{self.tile_directory}{x}.png", cv2.IMREAD_UNCHANGED)
        #     image = cv2.resize(image, (constants.TILE_SIZE, constants.TILE_SIZE))
        #     self.tile_list.append(image)
        for i in range(len(image_paths)):
            #print(image_paths[i])
            image = cv2.imread(image_paths[i], cv2.IMREAD_UNCHANGED)
            image = cv2.resize(image, (constants.TILE_SIZE, constants.TILE_SIZE))
            self.tile_list.append(image)

    def organize_tiles(self, num_tiles_displayed):
        num_rows = math.ceil(len(self.tile_list) / num_tiles_displayed)
        for i in range(0, num_rows):
            #print(f"the range({i * num_tiles_displayed}, {i * num_tiles_displayed + num_tiles_displayed}) ")
            temp = []
            for j in range((i * num_tiles_displayed), min(i * num_tiles_displayed + num_tiles_displayed, len(self.tile_list))):
                
                temp.append(self.tile_list[j])
            self.tile_menu_organized.append(temp)

        #print(f"organized:\n{self.tile_menu_organized}")
        #print(f"size of organized tile list = {len(self.tile_menu_organized)}")


    
            
    def draw_tiles(self, window, index):
        cur_window = window.copy()
        self.tile_loc.clear()
        for i in range(len(self.tile_menu_organized[index])):
            x_coor = constants.TILE_MENU_OFFSET_X + (constants.TILE_MENU_BTN_SPACING * (i)) + ((i) * constants.TILE_SIZE)
            result = SceneManager.overlay_image(cur_window, self.tile_menu_organized[index][i], (x_coor, constants.TILE_MENU_YLOC))
            cur_window = result
            self.tile_loc.append((x_coor, constants.TILE_MENU_YLOC))

        return cur_window





        