import arcade

from random import choice, randint

from config import *
from .weapon import Weapon


class Chest(arcade.Sprite):
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

        self.interacteble_area = 30 # на сколько надо подойти чтобы открыть
        self.is_open = False
        self.rarity = rarity
        self.chest_type = chest_type

        # Отдельный спрайт-триггер для коллизий
        self.trigger = arcade.SpriteCircle(self.interacteble_area, arcade.color.WHITE)
        self.trigger.alpha = 0  # невидимый
        self.trigger.center_x = center_x
        self.trigger.center_y = center_y

    def update(self):
        # Держим триггер на позиции сундука
        self.trigger.center_x = self.center_x
        self.trigger.center_y = self.center_y

    def open(self):
        self.is_open = True

    def get_item(self):
        if self.chest_type == "weapon":
            # айтем падает чуть в стороне от сундука
            return Weapon(center_x=int(self.center_x + randint(20, 40) * choice([-1, 1])), center_y=int(self.center_y + randint(20, 40) * choice([-1, 1])), type = 'axe')

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
