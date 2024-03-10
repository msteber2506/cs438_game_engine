import numpy as np
import cv2

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000

class EditorWindow:
    def __init__(self, shape, color=(0,0,0)):
        self.shape = shape
        self.window = np.full((shape[0], shape[1], 3), color, dtype=np.uint8)
        

    