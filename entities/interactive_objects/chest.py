import arcade

from random import choice, randint

from config import *
from ..weapon import Weapon
from .object import InetactiveObject


class Chest(InetactiveObject):
    def __init__(self, scale=1, center_x=0, center_y=0, rarity='normal', chest_type='weapon'):
        '''
            rarity - редкость,
            weapon - тип сундука, с обилками, с оружием и прочее
        '''
        super().__init__(None, scale, center_x, center_y)

        # Временная зелёная текстура
        self.texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.GREEN, outer_alpha=255)
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.is_open = False
        self.rarity = rarity
        self.chest_type = chest_type

        self.tips_text = 'E - open'

    def use(self):
        if not self.is_open:
            self.is_open = True
            self.interaction = False
            return self.get_item()

    def get_item(self):
        if self.chest_type == "weapon":
            # айтем падает чуть в стороне от сундука
            return Weapon(
                center_x=int(self.center_x + randint(20, 40) * choice([-1, 1])),
                center_y=int(self.center_y + randint(20, 40) * choice([-1, 1])),
                type = 'shotgun'
            )

        return None


def get_random_chest():
    rarity = choice(RARYTIES)
    chest_type = choice(CHEST_TYPES)

    return Chest(rarity=rarity, chest_type=chest_type)

def get_normal_chest():
    ...

def get_rare_chest():
    ...

def get_legend_chest():
    ...
