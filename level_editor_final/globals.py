from tile_menu import TileMenu
from scene_manager import SceneManager
import constants
from background import Background
from window import EditorWindow
from tile_map import TileMap
import numpy as np
import cv2


# from pathlib import Path
# def find_image_files(directory):
#     dir_path = Path(directory)

#     image_files = sorted(dir_path.glob('**/*.png'))

#     image_paths = [str(file.resolve()) for file in image_files]

#     return image_paths


#image_paths = find_image_files(constants.BACKGROUND_IMAGES_DIRECTORY)
image_paths = SceneManager.find_image_files(constants.BACKGROUND_IMAGES_DIRECTORY)

# for path in image_paths:
#     print(path)


# coordinates = [
#     (0, 0),
#     (0, constants.WINDOW_HEIGHT - 254 - 300),
#     (0, constants.WINDOW_HEIGHT - 296 - 150),
#     (0, constants.WINDOW_HEIGHT - 398)
# ]



background_info = dict(zip(image_paths, constants.BG_IMAGE_COORDINATES))


    
# sky_img_path = "./img/background/a1_sky_cloud.png"
# mountain_img_path = "./img/background/a2_mountain.png"
# pine1_img_path = "./img/background/a3_pine1.png"
# pine2_img_path = "./img/background/a4_pine2.png"

# background_info = {
#     sky_img_path: (0, 0),
#     mountain_img_path: (0, constants.WINDOW_HEIGHT - 254 - 300),
#     pine1_img_path: (0, constants.WINDOW_HEIGHT - 296 - 150),
#     pine2_img_path: (0, constants.WINDOW_HEIGHT - 398), 

# }

virtual_window_position = 0
start_index = 0
menu_index = 0
tile_btn_selected = [-1]
tile_selected_organized_index = None
save_btn = cv2.imread("./img/save_btn.png")
load_btn = cv2.imread("./img/load_btn.png")


window = EditorWindow((constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH), constants.LIGHT_BLUE)

tile_menu = TileMenu(constants.TILE_IMAGE_DIRECTORY)
tile_menu.load_tiles()
tile_menu.organize_tiles(constants.TILES_DISPLAYED_NUM)

tile_map = TileMap((constants.TILE_MAP_FULL_ROWS, constants.TILE_MAP_FULL_COLS))
#create ground
for tile in range(0, constants.TILE_MAP_FULL_COLS):
    tile_map.map_data[constants.TILE_MAP_FULL_ROWS - 1][tile] = 0


small_bg = SceneManager.create_background(background_info)
full_bg = Background(small_bg, constants.TILE_MAP_FULL_WIDTH)
