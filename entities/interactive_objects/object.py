import arcade

from config import *
from scripts import Trigger

class InetactiveObject(arcade.Sprite):
    def __init__(self, path_or_texture=None, scale=1, center_x=0, center_y=0):
        super().__init__(path_or_texture, scale, center_x, center_y)
        
        self.texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.YELLOW_ROSE, outer_alpha=255)
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.trigger = Trigger(
            None, self.scale, center_x, center_y
        )

    def update(self, delta_time: float=1 / 60):
        ...

    def draw(self):
        ...

    def use(self):
        ...
