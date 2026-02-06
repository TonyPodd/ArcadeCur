import arcade
import random

from config import *
from .object import InetactiveObject
from ..weapon import Weapon


class StoreCounter(InetactiveObject):
    def __init__(self, scale=1, center_x=0, center_y=0):
        super().__init__(None, scale, center_x, center_y)
        self.texture = arcade.make_soft_square_texture(TILE_SIZE, (222, 124, 4), outer_alpha=255)
        
        self.tips_text = 'E - купить'
        self.cost = random.randint(500, 700)
        
        weapon_pool = [k for k in WEAPON_TYPES.keys() if k != "boss_staff"]
        weapon_type = random.choice(weapon_pool) if weapon_pool else random.choice(list(WEAPON_TYPES.keys()))
        self.item = Weapon(
            1, self.center_x, self.center_y, weapon_type
        )
        self.item.is_on_floor = False

    def draw_item(self):
        if self.interaction == True:
            arcade.draw_sprite(self.item)

    def draw_ui(self):
        """ Отрисовак всех интерфейсов """
        if self.interaction:
            arcade.draw_text(
                f'Цена:{self.cost}',
                self.center_x - self.width / 2 + 2,
                self.center_y + 14,
                arcade.color.WHITE,
            )


    def draw_tips(self):
        if self.interaction:
            super().draw_tips()

    def use(self, value: int):
        """ Покупка предмета """

        if value < self.cost:
            return (0, None)
        self.interaction = False

        return (self.cost, self.item)
