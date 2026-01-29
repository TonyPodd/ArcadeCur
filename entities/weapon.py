import arcade

from config import *
from .item import Item
from .bullet import Bullet
from math import degrees

class Weapon(Item):
    def __init__(self, scale=1, center_x=0, center_y=0, type='default_gun'):
        super().__init__(scale, center_x, center_y)

        self.bullets = arcade.SpriteList()
        self.can_shoot = True
        self.shoot_timeout = WEAPON_TYPES[type]["shoot_timeout"] # Время между выстрелами
        self.damage = WEAPON_TYPES[type]["damage"]
        self.bullet_radius = WEAPON_TYPES[type]["bullet_radius"]
        self.bullet_speed = WEAPON_TYPES[type]["bullet_speed"]


    def shoot(self):
        if self.can_shoot:
            self.can_shoot = False
            arcade.schedule_once(self.update_can_shoot, self.shoot_timeout)
            temp_bullet = Bullet()
            temp_bullet.center_x = self.center_x
            temp_bullet.center_y = self.center_y
            temp_bullet.damage = self.damage
            temp_bullet.bullet_radius = self.bullet_radius
            temp_bullet.bullet_speed = self.bullet_speed
            # temp_bullet.dir_angel = self.angle
            temp_bullet.angle = - degrees(self.angle)


            return temp_bullet

        else:
            return None

    def update_can_shoot(self, timer):
        self.can_shoot = True


def get_default_gun():
    return Weapon(type='default_gun')

def get_normal_weapon():
    ...

def get_rare_weapon():
    ...

def get_legend_weapon():
    ...
