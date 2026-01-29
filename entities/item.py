import arcade

from config import *
from math import degrees, cos, sin

class Item(arcade.Sprite):
    def __init__(self, scale=1, center_x=0, center_y=0, type=''):
        super().__init__(":resources:images/topdown_tanks/tankDark_barrel3_outline.png", scale, center_x, center_y)

        self.is_on_floor = True
        self.can_interact = False
        self.player = None
        self.name = ''
        self.clas = ''
        self.angle = 0
        self.direct_angle = 0

    def update(self):
        if self.player:
            self.center_x = self.player.center_x
            self.center_y = self.player.center_y
            self.direct_angle = -degrees(self.player.view_angle)
            self.angle = -degrees(self.player.view_angle) + 90
            # print(self.player.view_angle)

        # print(self.center_x, self.center_y)

    def drop(self):
        self.player = None
        self.is_on_floor = True
        self.can_interact = True

    def grab(self, player):
        self.player = player
        self.is_on_floor = False
        self.can_interact = False

    def draw(self):
        distance = 28
        x = self.player.center_x + cos(self.player.view_angle) * distance
        y = self.player.center_y + sin(self.player.view_angle) * distance

        # Рисуем сам спрайт предмета поверх игрока в направлении взгляда
        self.center_x = x
        self.center_y = y
        arcade.draw_sprite(self)