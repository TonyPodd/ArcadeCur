import arcade

from config import *


class Wall(arcade.Sprite):
    def __init__(self, path_or_texture=None, scale=1, center_x=0, center_y=0):
        super().__init__(path_or_texture, scale, center_x, center_y)
        
        # Временный квадрат вместо спрайта
        self.texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.GRAY, outer_alpha=255)
        
        self.width = TILE_SIZE
        self.height = TILE_SIZE