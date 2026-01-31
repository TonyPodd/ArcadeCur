import arcade

from config import *


class Floor(arcade.Sprite):
    def __init__(self, path_or_texture=None, scale=1, center_x=0, center_y=0):
        super().__init__(path_or_texture, scale, center_x, center_y)

        self.texture = arcade.make_soft_square_texture(40, arcade.color.GRAY_ASPARAGUS, outer_alpha=255)

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.room_number = None
