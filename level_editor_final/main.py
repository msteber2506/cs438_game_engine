import numpy 
import cv2

from window import EditorWindow
from scene_manager import SceneManager
from background import Background
from tile_map import TileMap
import constants
import input_map
import globals





cv2.namedWindow(constants.WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(constants.WINDOW_NAME, input_map.mouse_callback)
input_map.construct_scene()


while True:

    #key = cv2.waitKey(30) & 0xFF
    key = cv2.waitKeyEx(30) & 0xFF
    if key == 27:
        break
    elif key in input_map.input_map:
        #input_map.input_map[key](full_bg, window, key == ord("r"))
        #input_map.input_map[key](globals.full_bg, globals.window, key == ord("r"))
        input_map.input_map[key]()

        input_map.construct_scene()
        
    
    
    
cv2.destroyAllWindows()