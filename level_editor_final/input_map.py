import cv2
import numpy
import constants
from scene_manager import SceneManager
import globals
import numpy as np
import pickle
import math


def draw_rect_border(window, image, coordinates, color=[0, 0, 255, 255], thickness=1):
    x, y = coordinates
    col = window.shape[2]
    height = image.shape[0]
    width = image.shape[1]
    new_window = window.copy()

    # #vertical left line
    
    # new_window[y:(y+height), x] = np.full((height,col), color)

    # #vertical right line
    # new_window[y:(y+height), (x + width)] = np.full((height,col), color)

    # #horizontal top line
    
    # new_window[y, (x-1):(x + width + 2)] = np.full((width + 3,col), color)


    # #horizontal bottom line
    # new_window[(y+height-1), (x-1):(x + width + 2)] = np.full((width + 3,col), color)

    #top line
    new_window[y - thickness:y, x - thickness:x + width + thickness] = color

    #bottom
    new_window[y + height:y + height + thickness, x - thickness:x + width + thickness] = color

    #left
    new_window[y:y + height, x - thickness:x] = color

    #right
    new_window[y:y + height, x + width:x + width + thickness] = color

    

    return new_window

def scroll(full_image, virtual_window_position, window_width):
    full_bg = full_image.copy()
    window_end = virtual_window_position + window_width

    
    return full_bg[:, virtual_window_position:window_end]



def construct_scene():
    
    new_scene = SceneManager.draw_world(globals.full_bg.full_background, globals.tile_map.map_data, globals.tile_menu.tile_list)
   
    new_scene = scroll(new_scene, globals.virtual_window_position, constants.WINDOW_WIDTH)

    new_scene = SceneManager.draw_grid(new_scene, constants.LIGHT_BLUE)
    new_scene = SceneManager.overlay_image(globals.window.window, new_scene, (0,0))
    new_scene = globals.tile_menu.draw_tiles(new_scene, globals.menu_index)

    if globals.tile_btn_selected[0] > -1 and globals.tile_selected_organized_index != None:
        #print(f"globals.tile_btn_selected[0] = {globals.tile_btn_selected[0]}")
        #print(f"globals.tile_btn_selected[0] = {globals.tile_btn_selected[0]}")
       #print(f"globals.tile_menu.tile_menu_organized[globals = {globals.tile_menu.tile_menu_organized[globals.menu_index][globals.tile_btn_selected[0]]}")
        #print(f"globals.menu_index = {globals.menu_index}")
        #print(f"globals.tile_menu.tile_loc[tile_selected] = {globals.tile_menu.tile_loc[tile_selected]}")
        #print(f"tile_selected = {globals.tile_selected_organized_index}")
        new_scene = draw_rect_border(new_scene, globals.tile_menu.tile_menu_organized[globals.menu_index][globals.tile_selected_organized_index], globals.tile_menu.tile_loc[globals.tile_selected_organized_index], [255, 0, 0, 255], 4)
    new_scene = SceneManager.overlay_image(new_scene, globals.save_btn, (constants.SAVE_BTN_X, constants.SAVE_BTN_Y))
    new_scene = SceneManager.overlay_image(new_scene, globals.load_btn, (constants.LOAD_BTN_X, constants.LOAD_BTN_Y))
    SceneManager.render(constants.WINDOW_NAME, new_scene, (constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))

def scroll_render(isScrollToRight):
    if isScrollToRight:
        if globals.virtual_window_position + constants.SCROLL_AMOUNT <= globals.full_bg.full_background.shape[1] - constants.WINDOW_WIDTH:
            globals.virtual_window_position += constants.SCROLL_AMOUNT

            construct_scene()

            
    else:
        if globals.virtual_window_position - constants.SCROLL_AMOUNT >= 0:
            globals.virtual_window_position -= constants.SCROLL_AMOUNT

            construct_scene()
    
def tile_menu_move_right(full_bg, window):
    #print(f"math.ceil(constants.TILE_TYPES // constants.TILES_DISPLAYED_NUM) = {math.ceil(constants.TILE_TYPES / constants.TILES_DISPLAYED_NUM)}")
    #print(f"constants.TILE_TYPES // constants.TILES_DISPLAYED_NUM = {constants.TILE_TYPES / constants.TILES_DISPLAYED_NUM}")
    if globals.menu_index + 1 < math.ceil(constants.TILE_TYPES / constants.TILES_DISPLAYED_NUM) :
        globals.menu_index += 1
        globals.tile_btn_selected = [-1]
        #print(f"menu_index in right scroll = {globals.menu_index}")


        construct_scene()

    

    

def tile_menu_move_left(full_bg, window):
    
    
    if globals.menu_index - 1 >= 0:
        globals.menu_index -= 1
        globals.tile_btn_selected = [-1]
        construct_scene()
        


   

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"clicked at position (x={x}, y={y})")
        # print(f"virtual_window_position = {globals.virtual_window_position}")
        col = (x + globals.virtual_window_position) // constants.TILE_SIZE
        row = y // constants.TILE_SIZE
        print(f"Tile ({row},{col})")
        
        for i in range(len(globals.tile_menu.tile_loc)):

            
            if x >= globals.tile_menu.tile_loc[i][0] and x <= (globals.tile_menu.tile_loc[i][0] + constants.TILE_SIZE) and y >= globals.tile_menu.tile_loc[i][1] and y <= (globals.tile_menu.tile_loc[i][1] + constants.TILE_SIZE):
                #print(f"clicked on tile menu item")

                
                globals.tile_btn_selected[0] = (globals.menu_index * constants.TILES_DISPLAYED_NUM) + i
                globals.tile_selected_organized_index = i
                #print(f"clicked {globals.tile_btn_selected}")
                #print(f"tile btn selected = {globals.tile_btn_selected[0]}")
                #print(globals.tile_menu.tile_loc)
                # print("here it is",globals.tile_menu.tile_loc[-1])
                construct_scene()
                #print(f"current tile that is selected: tile {globals.tile_btn_selected[0]}")

        if x < constants.TILE_MAP_SCREEN_WIDTH and y < constants.TILE_MAP_SCREEN_HEIGHT:
            #print(f'inside tilemap')
            if globals.tile_map.map_data[row][col] >= 0:
                globals.tile_map.map_data[row][col] = -1
                ##print(f"true")
                
            else:
                globals.tile_map.map_data[row][col] = globals.tile_btn_selected[0]
                
            
            construct_scene()

        if x >= constants.SAVE_BTN_X and x <= (constants.SAVE_BTN_X + globals.save_btn.shape[1]) and y >= constants.SAVE_BTN_Y and y <= (constants.SAVE_BTN_Y + globals.save_btn.shape[0]):
            print(f"clicked save btn")
            output_file = open(constants.LEVEL_MAP_FILENAME, 'wb')
            pickle.dump(globals.tile_map.map_data, output_file)
            output_file.close()
        elif x >= constants.LOAD_BTN_X and x <= (constants.LOAD_BTN_X + globals.load_btn.shape[1]) and y >= constants.LOAD_BTN_Y and y <= (constants.LOAD_BTN_Y + globals.load_btn.shape[0]): 
            print(f"clicked load btn")
            globals.tile_map.map_data.clear()
            input_file = open(constants.LEVEL_MAP_FILENAME, 'rb')
            globals.tile_map.map_data = pickle.load(input_file)
            
            construct_scene()
        
    



input_map = {
        ord('d'): lambda: scroll_render(True),
        ord('a'): lambda: scroll_render(False),
        ord('n'): lambda: tile_menu_move_left(globals.full_bg, globals.window),
        ord('m'): lambda: tile_menu_move_right(globals.full_bg, globals.window)

}