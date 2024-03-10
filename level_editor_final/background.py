import numpy as np
import cv2
from scene_manager import SceneManager


class Background:
    def __init__(self, window, map_width_px):
        #the image list assumes the images are ordered from what will be starting at the bottom top
        new_window = window.copy()
        self.background = new_window
        self.full_background = SceneManager.create_full_background(self.background, map_width_px)