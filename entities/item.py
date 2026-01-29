import arcade

from config import *


class Item(arcade.Sprite):
    def __init__(self, scale=1, center_x=0, center_y=0, type=''):
        super().__init__(":resources:images/items/coinGold.png", scale, center_x, center_y)

        self.is_on_floor = True
        self.can_interact = False
        self.player = None
        self.name = '202'
        self.angle = 0

    def update(self):
        if self.player:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
            self.angle = self.player.view_angle

        # print(self.center_x, self.center_y)

    def drop(self):
        self.player = None
        self.is_on_floor = True
        self.can_interact = True

    def grab(self, player):
        self.player = player
        self.is_on_floor = False
        self.can_interact = False
