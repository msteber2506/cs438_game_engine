import numpy as np
import cv2
import constants

class TileMap:
    def __init__(self, shape):
        rows, cols = shape
        self.map_data = [[-1] * constants.TILE_MAP_FULL_COLS for _ in range(constants.TILE_MAP_FULL_ROWS)]

        # self.full_background = full_background

    
