import arcade

from config import *


class Weapon(arcade.Sprite):
    def __init__(self, scale=1, center_x=0, center_y=0, type='default_gun'):
        super().__init__(None, scale, center_x, center_y)

        self.width = TILE_SIZE
        self.height = TILE_SIZE


def get_default_gun():
    return Weapon(type='default_gun')

def get_normal_weapon():
    ...

def get_rare_weapon():
    ...

def get_legend_weapon():
    ...
