import arcade

from config import *


class Door(arcade.Sprite):
    def __init__(self, scale=1, center_x=0, center_y=0):
        super().__init__(None, scale, center_x, center_y)
        
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        self.is_close = False  # Закртыта ли дверь
    
    def close_door(self):
        self.is_close = True
