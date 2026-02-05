import arcade

from config import *
from utils.procedural_textures import plank_texture, _tint


class Door(arcade.Sprite):
    def __init__(self, scale=1, center_x=0, center_y=0):
        super().__init__(None, scale, center_x, center_y)
        self.texture = plank_texture(TILE_SIZE, DOOR_OPEN_COLOR, _tint(DOOR_OPEN_COLOR, 0.7))
        
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        self.is_close = False  # Закртыта ли дверь
    
    def close_door(self):
        self.is_close = True
        self.texture = plank_texture(TILE_SIZE, DOOR_CLOSED_COLOR, _tint(DOOR_CLOSED_COLOR, 0.7))

    def open_door(self):
        self.is_close = False
        self.texture = plank_texture(TILE_SIZE, DOOR_OPEN_COLOR, _tint(DOOR_OPEN_COLOR, 0.7))
