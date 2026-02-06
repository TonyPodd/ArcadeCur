import arcade

from config import *
from .item import Item
from .bullet import Bullet
from math import degrees, cos, sin, radians
import random
import time

from utils.procedural_textures import weapon_texture, _tint, sword_texture, axe_texture, gun_texture

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
        self.last_shot_time = 0.0
        self.handle_offset = 0.0
        self.apply_procedural_texture(type)
        self.weapon_type = type


    def shoot(self):
        if self.can_shoot:
            self.can_shoot = False
            arcade.schedule_once(self.update_can_shoot, self.shoot_timeout)
            bullets_to_return = []
            self.last_shot_time = time.time()
            if self.clas == "melee":
                self.melee_active_until = time.time() + MELEE_REFLECT_TIME
            for _ in range(self.shots_per_tick):
                temp_bullet = Bullet()
                temp_bullet.center_x = self.center_x
                temp_bullet.center_y = self.center_y
                temp_bullet.damage = self.damage
                temp_bullet.bullet_radius = self.bullet_radius
                temp_bullet.bullet_speed = self.bullet_speed

                if self.clas == "gun":
                    temp_bullet.damage_type = 'bullet'
                elif self.clas == "magic":
                    temp_bullet.damage_type = 'magic'
                else:
                    temp_bullet.damage_type = 'hit'
                temp_bullet.variant = self.weapon_type
                temp_bullet.size_scale = None
                temp_bullet.apply_stats()
                temp_bullet.update_texture()


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
                    temp_bullet.alpha = 0
                bullets_to_return.append(temp_bullet)

            return bullets_to_return

        else:
            return None

    def is_melee_active(self):
        return self.clas == "melee" and time.time() < self.melee_active_until

    def update_can_shoot(self, timer):
        self.can_shoot = True

    def apply_procedural_texture(self, weapon_type):
        base = (80, 80, 90)
        outline = _tint(base, 0.6)
        barrel = _tint(base, 1.2)
        grip = _tint(base, 0.9)

        if weapon_type in ("pistol", "default_gun"):
            size = 24
            stock = _tint(base, 0.8)
            self.texture = gun_texture(size, base, outline, barrel, grip, stock, profile="pistol")
            self.handle_offset = size * 0.15
        elif weapon_type == "rifle":
            size = 30
            stock = _tint(base, 0.7)
            self.texture = gun_texture(size, _tint(base, 0.95), outline, barrel, grip, stock, profile="rifle")
            self.handle_offset = size * 0.28
        elif weapon_type == "smg":
            size = 22
            stock = _tint(base, 0.75)
            self.texture = gun_texture(size, _tint(base, 0.9), outline, barrel, _tint(grip, 0.85), stock, profile="pistol")
            self.handle_offset = size * 0.12
        elif weapon_type == "burst_rifle":
            size = 28
            stock = _tint(base, 0.7)
            self.texture = gun_texture(size, _tint(base, 0.95), outline, barrel, grip, stock, profile="rifle")
            self.handle_offset = size * 0.26
        elif weapon_type == "shotgun":
            size = 28
            stock = _tint(base, 0.85)
            self.texture = gun_texture(size, _tint(base, 0.9), outline, barrel, _tint(grip, 0.9), stock, profile="shotgun")
            self.handle_offset = size * 0.24
        elif weapon_type == "sniper":
            size = 32
            stock = _tint(base, 0.7)
            self.texture = gun_texture(size, _tint(base, 0.85), outline, _tint(barrel, 1.1), grip, stock, profile="sniper")
            self.handle_offset = size * 0.32
        elif weapon_type == "heavy_rifle":
            size = 32
            stock = _tint(base, 0.65)
            self.texture = gun_texture(size, _tint(base, 0.8), outline, _tint(barrel, 1.15), _tint(grip, 0.9), stock, profile="rifle")
            self.handle_offset = size * 0.3
        elif weapon_type == "railgun":
            size = 34
            stock = _tint(base, 0.6)
            self.texture = gun_texture(size, _tint(base, 0.75), outline, _tint(barrel, 1.3), _tint(grip, 0.8), stock, profile="sniper")
            self.handle_offset = size * 0.33
        elif weapon_type == "orb":
            size = 26
            staff = _tint((120, 80, 160), 1.0)
            glow = _tint((200, 140, 255), 1.0)
            self.texture = weapon_texture(size - 8, size, staff, _tint(staff, 0.7), glow, _tint(staff, 0.9))
            self.handle_offset = size * 0.28
        elif weapon_type == "fire_wand":
            size = 26
            staff = _tint((160, 90, 60), 1.0)
            glow = _tint((255, 140, 80), 1.0)
            self.texture = weapon_texture(size - 8, size, staff, _tint(staff, 0.7), glow, _tint(staff, 0.9))
            self.handle_offset = size * 0.28
        elif weapon_type == "ice_wand":
            size = 26
            staff = _tint((90, 120, 180), 1.0)
            glow = _tint((170, 220, 255), 1.0)
            self.texture = weapon_texture(size - 8, size, staff, _tint(staff, 0.7), glow, _tint(staff, 0.9))
            self.handle_offset = size * 0.28
        elif weapon_type == "boss_staff":
            size = 32
            staff = _tint((120, 70, 90), 1.0)
            glow = _tint((255, 120, 160), 1.0)
            self.texture = weapon_texture(size - 6, size, staff, _tint(staff, 0.7), glow, _tint(staff, 0.9))
            self.handle_offset = size * 0.3
        elif weapon_type == "sword":
            size = 28
            blade = _tint((170, 180, 200), 1.0)
            self.texture = sword_texture(size, blade, _tint(blade, 0.7), _tint((120, 80, 50), 1.0), _tint((90, 60, 40), 1.0))
            self.handle_offset = size * 0.4
        elif weapon_type == "dagger":
            size = 22
            blade = _tint((190, 200, 210), 1.0)
            self.texture = sword_texture(size, blade, _tint(blade, 0.7), _tint((120, 80, 50), 1.0), _tint((90, 60, 40), 1.0))
            self.handle_offset = size * 0.35
        elif weapon_type == "axe":
            size = 28
            head = _tint((190, 200, 210), 1.0)
            self.texture = axe_texture(size, head, _tint(head, 0.7), _tint((120, 80, 50), 1.0))
            self.handle_offset = size * 0.4
        elif weapon_type == "hammer":
            size = 30
            head = _tint((180, 190, 200), 1.0)
            self.texture = axe_texture(size, head, _tint(head, 0.7), _tint((110, 70, 40), 1.0))
            self.handle_offset = size * 0.42
        else:
            size = (26, 10)
            self.texture = weapon_texture(size[0], size[1], base, outline, barrel, grip)
            self.handle_offset = size[0] * 0.2
        if hasattr(self, "texture_sprite") and self.texture_sprite:
            self.texture_sprite.texture = self.texture
        self.weapon_type = weapon_type

    def draw(self):
        if not self.player:
            arcade.draw_sprite(self)
            return

        base_angle = getattr(self.player, "view_angle", 0.0)
        now = time.time()
        recoil = 0.0
        if self.clas != "melee" and now - self.last_shot_time < 0.12:
            t = 1.0 - (now - self.last_shot_time) / 0.12
            recoil = max(0.0, t) * 4.0

        swing_progress = None
        if self.clas == "melee" and self.is_melee_active():
            remaining = max(0.0, self.melee_active_until - now)
            swing_progress = 1.0 - min(1.0, remaining / max(MELEE_REFLECT_TIME, 0.05))
            swing_progress = 1.0 - (1.0 - swing_progress) ** 2

        if swing_progress is not None:
            sweep = radians(90)
            base_angle = base_angle - sweep / 2 + sweep * swing_progress

        base_dist = 0.2 * (self.player.width if hasattr(self.player, "width") else 40)
        distance = max(18, base_dist + self.handle_offset) - recoil
        x = self.player.center_x + cos(base_angle) * distance
        y = self.player.center_y + sin(base_angle) * distance
        self.center_x = x
        self.center_y = y
        # Поворачиваем спрайт синхронно с направлением взгляда
        self.angle = - degrees(base_angle) 
        arcade.draw_sprite(self)

        if swing_progress is not None:
            length = max(self.bullet_radius, 12) + 18
            width = 10 + 6 * (1 - abs(swing_progress - 0.5) * 2)
            dx = cos(base_angle)
            dy = sin(base_angle)
            tip_x = self.player.center_x + dx * (length + 10)
            tip_y = self.player.center_y + dy * (length + 10)
            base_x = self.player.center_x + dx * (length - 10)
            base_y = self.player.center_y + dy * (length - 10)
            px = -dy
            py = dx
            left_x = base_x + px * width
            left_y = base_y + py * width
            right_x = base_x - px * width
            right_y = base_y - py * width
            alpha = int(210 * (1 - abs(swing_progress - 0.5) * 1.4))
            color = (255, 220, 130, max(40, alpha))
            arcade.draw_triangle_filled(
                tip_x, tip_y,
                left_x, left_y,
                right_x, right_y,
                color
            )


def get_default_gun():
    return Weapon(type='default_gun')

def get_normal_weapon():
    ...

def get_rare_weapon():
    ...

def get_legend_weapon():
    ...
