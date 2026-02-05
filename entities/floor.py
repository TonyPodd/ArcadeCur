import arcade

from config import *
from utils.procedural_textures import floor_texture, _tint


class Floor(arcade.Sprite):
    def __init__(self, path_or_texture=None, scale=1, center_x=0, center_y=0):
        super().__init__(path_or_texture, scale, center_x, center_y)

        accent = _tint(FLOOR_COLOR, 0.85)
        self.texture = floor_texture(TILE_SIZE, FLOOR_COLOR, accent)

        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.room_number = None
