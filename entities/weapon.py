import arcade

from config import *
from .item import Item
from .bullet import Bullet
from math import degrees, cos, sin, radians
import random
import time

class Weapon(Item):
    def __init__(self, scale=1, center_x=0, center_y=0, type='default_gun', clas = 'gun'):
        super().__init__(scale, center_x, center_y)
        self.bullets = arcade.SpriteList()
        self.clas = WEAPON_TYPES[type]["weapon_type"]
        self.can_shoot = True
        self.shoot_timeout = WEAPON_TYPES[type]["shoot_timeout"] # Время между выстрелами
        self.name = WEAPON_TYPES[type]["name"]
        self.damage = WEAPON_TYPES[type]["damage"]
        self.damage_type = WEAPON_TYPES[type]["damage_type"]
        self.bullet_radius = WEAPON_TYPES[type]["bullet_radius"]
        self.bullet_speed = WEAPON_TYPES[type]["bullet_speed"]
        self.shots_per_tick = WEAPON_TYPES[type]["shots_per_tick"]
        self.spread = WEAPON_TYPES[type].get("spread", 0)
        self.melee_active_until = 0.0


    def shoot(self):
        if self.can_shoot:
            self.can_shoot = False
            arcade.schedule_once(self.update_can_shoot, self.shoot_timeout)
            bullets_to_return = []
            if self.clas == "melee":
                self.melee_active_until = time.time() + MELEE_REFLECT_TIME
            for _ in range(self.shots_per_tick):
                temp_bullet = Bullet()
                temp_bullet.center_x = self.center_x
                temp_bullet.center_y = self.center_y
                temp_bullet.damage = self.damage
                temp_bullet.damage_type = self.damage_type
                temp_bullet.bullet_radius = self.bullet_radius
                temp_bullet.bullet_speed = self.bullet_speed
                temp_bullet.apply_stats()
                
                if self.clas == "gun":
                    temp_bullet.damage_type = 'bullet'
                elif self.clas == "magic":
                    temp_bullet.damage_type = 'magic'
                else:
                    temp_bullet.damage_type = 'hit'


                # temp_bullet.dir_angel = self.angle
                spread_offset = random.uniform(-self.spread, self.spread)
                temp_bullet.angle = self.direct_angle + spread_offset

                if self.clas == "melee":
                    base_x = self.player.center_x if self.player else self.center_x
                    base_y = self.player.center_y if self.player else self.center_y
                    distance = max(self.bullet_radius, 8)
                    temp_bullet.center_x = base_x + cos(radians(temp_bullet.angle)) * distance
                    temp_bullet.center_y = base_y + sin(radians(temp_bullet.angle)) * -distance
                    temp_bullet.speed = 0
                    temp_bullet.life_frames = 2
                bullets_to_return.append(temp_bullet)

            return bullets_to_return

        else:
            return None

    def is_melee_active(self):
        return self.clas == "melee" and time.time() < self.melee_active_until

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
