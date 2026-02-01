import arcade

import config
from .weapon import Weapon

class Enemy(arcade.Sprite):
    def __init__(self, x: float, y: float, type = "recrut"):
        super().__init__()

        # settings
        self.type = type
        self.is_dead = False  # Умер ли енеми
        self.hp = config.ENEMY_TYPES[self.type]['hp']
        self.max_speed = config.ENEMY_TYPES[self.type]['speed']
        self.agr_radius = config.ENEMY_TYPES[self.type]['arg_range']
        self.attack_radius = config.ENEMY_TYPES[self.type]['attack_range']
        self.weapon_name = config.ENEMY_TYPES[self.type]['weapon']
        self.weapon_type = config.WEAPON_TYPES[self.weapon_name]['weapon_type']
        self.weapon = Weapon(center_x=int(self.center_x), center_y= int(self.center_y), type=self.weapon_name, clas= self.weapon_type)

        self.is_player_visible = False
        

        # Временный квадрат вместо спрайта
        self.texture = arcade.make_soft_square_texture(40, arcade.color.RED, outer_alpha=255)
        self._hit_box._points = ((-20, -15), (20, -15), (20, 15), (-20, 15))

        self.agr_trigger = arcade.SpriteCircle(self.agr_radius, arcade.color.WHITE)
        self.attack_trigger = arcade.SpriteCircle(self.agr_radius, arcade.color.RED_BROWN)


        self.center_x = x
        self.center_y = y


    def update(self):
        ...


    def move_to_player(self):
        ...
