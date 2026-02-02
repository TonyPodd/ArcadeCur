import arcade

from config import *


class Trigger(arcade.Sprite):
    def __init__(self, path_or_texture=None, scale=1, center_x=0, center_y=0):
        super().__init__(path_or_texture, scale, center_x, center_y)

        self.width = TILE_SIZE
        self.height = TILE_SIZE
        

    def set_size(self, width=None, height=None):
        if self.height is not None:
            self.height = height

        if self.width is not None:
            self.width = width
        print(self.width, self.height)
    
