import arcade

from config import *
from utils.procedural_textures import brick_texture, _tint


class Wall(arcade.Sprite):
    def __init__(self, path_or_texture=None, scale=1, center_x=0, center_y=0):
        super().__init__(path_or_texture, scale, center_x, center_y)
        
        mortar = _tint(WALL_COLOR, 0.6)
        self.texture = brick_texture(TILE_SIZE, WALL_COLOR, mortar)
        
        self.width = TILE_SIZE
        self.height = TILE_SIZE
