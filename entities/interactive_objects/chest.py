import arcade
import random

from random import choice, randint

from config import *
from utils.procedural_textures import chest_texture, _tint
from ..weapon import Weapon
from .object import InetactiveObject


class Chest(InetactiveObject):
    def __init__(self, scale=1, center_x=0, center_y=0, rarity='normal', chest_type='weapon'):
        '''
            rarity - редкость,
            weapon - тип сундука, с обилками, с оружием и прочее
        '''
        super().__init__(None, scale, center_x, center_y)

        # Самописные текстуры сундука
        self.texture_closed = chest_texture(
            TILE_SIZE,
            CHEST_COLOR,
            _tint(CHEST_COLOR, 0.6),
            _tint(CHEST_COLOR, 1.15),
            _tint(CHEST_COLOR, 1.35)
        )
        self.texture_open = chest_texture(
            TILE_SIZE,
            CHEST_OPEN_COLOR,
            _tint(CHEST_OPEN_COLOR, 0.6),
            _tint(CHEST_OPEN_COLOR, 1.2),
            _tint(CHEST_OPEN_COLOR, 1.4)
        )
        self.texture = self.texture_closed
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
            self.texture = self.texture_open
            return self.get_item()

    def get_item(self):
        weapon_pool = [k for k in WEAPON_TYPES.keys() if k != "boss_staff"]
        weapon_type = random.choice(weapon_pool) if weapon_pool else random.choice(list(WEAPON_TYPES.keys()))
        # weapon_type = 'axe'
        if self.chest_type == "weapon":
            # айтем падает чуть в стороне от сундука
            return Weapon(
                center_x=int(self.center_x + randint(20, 40) * choice([-1, 1])),
                center_y=int(self.center_y + randint(20, 40) * choice([-1, 1])),
                type=weapon_type
            )

        return None


def get_random_chest():
    rarity = choice(RARITIES)
    chest_type = choice(CHEST_TYPES)

    return Chest(rarity=rarity, chest_type=chest_type)

def get_normal_chest():
    ...

def get_rare_chest():
    ...

def get_legend_chest():
    ...
