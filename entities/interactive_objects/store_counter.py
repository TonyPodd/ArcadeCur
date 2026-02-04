import arcade
import random

from config import *
from .object import InetactiveObject
from ..item import Item


class StoreCounter(InetactiveObject):
    def __init__(self, scale=1, center_x=0, center_y=0):
        super().__init__(None, scale, center_x, center_y)
        self.texture = arcade.make_soft_square_texture(TILE_SIZE, (222, 124, 4), outer_alpha=255)
        
        self.tips_text = 'E - купить'
        self.cost = 400
        
        self.item = Item(
            1, self.center_x, self.center_y, 
        )

    def draw_item(self):
        arcade.draw_sprite(self.item)

    def draw_tips(self):
        if self.interaction:
            super().draw_tips()

    def buy(self):
        """ Покупка предмета """
