import arcade

from config import *
from .item import Item

class Weapon(Item):
    def __init__(self, scale=1, center_x=0, center_y=0, type='default_gun'):
        super().__init__(scale, center_x, center_y)

    def update(self):
        if (self.can_interact):
            ...
            # print("МОЖНО ПОДОБРАТЬ")

def get_default_gun():
    return Weapon(type='default_gun')

def get_normal_weapon():
    ...

def get_rare_weapon():
    ...

def get_legend_weapon():
    ...
