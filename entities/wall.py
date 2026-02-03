import arcade

from get_tiles import textures


class Wall(arcade.Sprite):
    def __init__(self, tile_id, scale=1, center_x=0, center_y=0):
        super().__init__(scale=scale, center_x=center_x, center_y=center_y)

        self.texture = textures[tile_id]

        self.width = 64
        self.height = 64


