import arcade

from config import *


class Door(arcade.Sprite):
    def __init__(self, scale=1, center_x=0, center_y=0):
        super().__init__(None, scale, center_x, center_y)
        self.texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.BRONZE_YELLOW, outer_alpha=255)
        
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        self.is_close = False  # Закртыта ли дверь
    
    def close_door(self):
        self.is_close = True
        self.texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.BROWN, outer_alpha=255)

    def open_door(self):
        self.is_close = False
        self.texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.BRONZE_YELLOW, outer_alpha=255)