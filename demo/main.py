import cv2 
import numpy as np
from render_engine import RenderingEngine, ImageProcessor, Sprite
import constants


#global variables
virtual_window_position = 0


# image = cv2.imread("./img/background/0.png", cv2.IMREAD_UNCHANGED)
# RenderingEngine.render_to_screen(constants.WINDOW_NAME, image, (image.shape[0], image.shape[1]))

map_data = RenderingEngine.load_pickled_data("./level0_map")
image_paths = RenderingEngine.find_image_files("./img/background/")
image_list = RenderingEngine.load_images(image_paths)

tile_paths = RenderingEngine.find_image_files("./img/tile/")
tile_list = RenderingEngine.load_images(tile_paths)


background_info = dict(zip(image_paths, constants.BG_IMAGE_COORDINATES))
partial_bg = RenderingEngine.create_background(background_info)
full_bg = RenderingEngine.create_full_background(partial_bg, constants.TILE_MAP_FULL_WIDTH)
scene = RenderingEngine.draw_world(full_bg, map_data, tile_list)

window = np.full((constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH, 3), constants.LIGHT_BLUE, dtype=np.uint8)
scene = RenderingEngine.overlay_image(window, scene, (0,0))
clean_map = scene.copy()
sprite_paths = RenderingEngine.find_image_files("./img/Player/Run/")
sprite_list = RenderingEngine.load_images(sprite_paths)
sprite = Sprite(sprite_paths, (0, full_bg.shape[0] - 3 * constants.TILE_SIZE))

scene = RenderingEngine.overlay_image(scene, sprite.sprite_images[0], (sprite.xloc, sprite.yloc))
RenderingEngine.render_to_screen(constants.WINDOW_NAME, scene, (constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))


while True:
    key = cv2.waitKeyEx(30)
    if key == 27:
        break
    elif key == ord('a'):
        #virtual_window_position = RenderingEngine.scroll_render(window,full_bg, map_data, tile_list, virtual_window_position, isScrollToRight=False)
        virtual_window_position = sprite.move("left", window,full_bg, map_data, tile_list, virtual_window_position, clean_map)
        #scene = RenderingEngine.overlay_image(clean_map, ImageProcessor.flip_image_y_axis(sprite.sprite_images[sprite.current_frame]), (sprite.xloc, sprite.yloc))
        #RenderingEngine.render_to_screen(constants.WINDOW_NAME, scene, (constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))
        
    elif key == ord('d'):
        #virtual_window_position = RenderingEngine.scroll_render(window,full_bg, map_data, tile_list, virtual_window_position, isScrollToRight=True)
        virtual_window_position = sprite.move("right", window,full_bg, map_data, tile_list, virtual_window_position, clean_map)
        #scene = RenderingEngine.overlay_image(clean_map, sprite.sprite_images[sprite.current_frame], (sprite.xloc, sprite.yloc))
        #RenderingEngine.render_to_screen(constants.WINDOW_NAME, scene, (constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))
    elif key == ord('p'):
        
        new_sprite = ImageProcessor.downscaling(sprite.sprite_images[sprite.current_frame], int(sprite.sprite_images[0].shape[0] * 0.5), int(sprite.sprite_images[0].shape[1] * 0.5))
        
        non_zero_pixels = np.any(new_sprite != 0, axis=2)


        alpha_channel = np.where(non_zero_pixels, 255, 0).astype(np.uint8)

        
        rgba_image = cv2.merge((new_sprite, alpha_channel))
        scene = RenderingEngine.overlay_image(clean_map, rgba_image, (sprite.xloc, sprite.yloc))
        RenderingEngine.render_to_screen(constants.WINDOW_NAME, scene, (constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))
    elif key == ord('o'):
        
        new_sprite = ImageProcessor.upscaling(sprite.sprite_images[sprite.current_frame], int(sprite.sprite_images[0].shape[0] * 1.5), int(sprite.sprite_images[0].shape[1] * 1.5))
        
        non_zero_pixels = np.any(new_sprite != 0, axis=2)


        alpha_channel = np.where(non_zero_pixels, 255, 0).astype(np.uint8)

        
        rgba_image = cv2.merge((new_sprite, alpha_channel))
        scene = RenderingEngine.overlay_image(clean_map, rgba_image, (sprite.xloc, sprite.yloc - constants.TILE_SIZE))
        RenderingEngine.render_to_screen(constants.WINDOW_NAME, scene, (constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH))

        
cv2.destroyAllWindows()