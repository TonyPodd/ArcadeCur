import arcade
from math import cos, sin, radians
from config import *
from PIL import Image, ImageDraw
import random


def _bullet_color(damage_type):
    if damage_type == "magic":
        return (140, 120, 240)
    if damage_type == "hit":
        return (255, 170, 90)
    return (235, 210, 140)

def _bullet_style(damage_type):
    if damage_type == "magic":
        return "magic"
    if damage_type == "hit":
        return "hit"
    return "bullet"


def _make_bullet_texture(size, color, style):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = max(1, size // 10)
    cx = size // 2
    if style == "magic":
        glow = (
            min(255, int(color[0] * 0.9)),
            min(255, int(color[1] * 0.9)),
            min(255, int(color[2] * 1.1)),
            150,
        )
        draw.ellipse([0, 0, size - 1, size - 1], fill=glow)
        draw.ellipse([pad, pad, size - pad - 1, size - pad - 1], fill=color)
        diamond = max(3, size // 4)
        points = [
            (cx, cx - diamond),
            (cx + diamond, cx),
            (cx, cx + diamond),
            (cx - diamond, cx),
        ]
        draw.polygon(points, fill=(255, 255, 255, 220))
    elif style == "streak":
        core_h = max(4, size // 4)
        draw.ellipse([0, cx - core_h, size - 1, cx + core_h], fill=color)
        draw.rectangle([2, cx - 1, size - 3, cx + 1], fill=(255, 255, 255, 220))
    elif style == "needle":
        draw.ellipse([0, cx - 2, size - 1, cx + 2], fill=color)
        draw.rectangle([2, cx - 1, size - 3, cx + 1], fill=(255, 255, 255, 180))
    elif style == "pellet":
        draw.ellipse([pad, pad, size - pad - 1, size - pad - 1], fill=color)
        draw.ellipse([cx - 2, cx - 2, cx + 2, cx + 2], fill=(255, 255, 255, 200))
    elif style == "hit":
        outer = (
            min(255, int(color[0] * 0.8)),
            min(255, int(color[1] * 0.7)),
            min(255, int(color[2] * 0.6)),
            160,
        )
        draw.ellipse([0, 0, size - 1, size - 1], fill=outer)
        draw.ellipse([pad, pad, size - pad - 1, size - pad - 1], fill=color)
        draw.rectangle([cx - 1, 2, cx + 1, size - 3], fill=(255, 220, 170, 220))
    else:
        outer = (
            min(255, int(color[0] * 0.8)),
            min(255, int(color[1] * 0.8)),
            min(255, int(color[2] * 0.8)),
            140,
        )
        draw.ellipse([0, 0, size - 1, size - 1], fill=outer)
        draw.ellipse([pad, pad, size - pad - 1, size - pad - 1], fill=color)
        core = max(3, size // 3)
        core_col = (
            min(255, int(color[0] * 1.2)),
            min(255, int(color[1] * 1.2)),
            min(255, int(color[2] * 1.2)),
            255,
        )
        draw.ellipse([cx - core, cx - core, cx + core, cx + core], fill=core_col)
    return arcade.Texture(img)

class Bullet(arcade.Sprite):
    _tex_cache = {}

    def __init__(self, scale=1, center_x=0, center_y=0):
        super().__init__(":resources:/images/space_shooter/laserBlue01.png", scale, center_x, center_y)

        self.speed = DEFAULT_BULLET_VELOCITY
        self.angle = 0
        self.damage = 20
        self.damage_type = ""
        self.bullet_radius = 0
        self.bullet_speed = 0
        self.life_frames = None
        # bullet исчезает после попадания, magic ебашит до стенки, hit - милишка, бьет всех пока не expired
        self.expired = False
        self.size_scale = None
        self.trail_color = None
        self.trail_length = None
        self.update_texture()

    def apply_stats(self):
        if self.bullet_speed:
            self.speed = self.bullet_speed
        if self.bullet_radius:
            size = self.bullet_radius * 2
            self.width = size
            self.height = size
        self.update_texture()

    def update_texture(self):
        if self.size_scale is None:
            self.size_scale = random.uniform(0.85, 1.2)
            if self.damage_type == "magic":
                self.size_scale = random.uniform(0.95, 1.35)
            variant = getattr(self, "variant", None)
            if variant == "shotgun":
                self.size_scale *= 0.65
            elif variant == "sniper":
                self.size_scale *= 1.15
            elif variant == "smg":
                self.size_scale *= 0.8
            elif variant == "heavy_rifle":
                self.size_scale *= 1.1
            elif variant == "railgun":
                self.size_scale *= 1.25
        base = self.bullet_radius * 2 + 10 if self.bullet_radius else 18
        size = max(16, int(base * self.size_scale))
        color = _bullet_color(self.damage_type)
        style = _bullet_style(self.damage_type)
        variant = getattr(self, "variant", None)
        if style == "bullet":
            if variant == "shotgun":
                style = "pellet"
            elif variant in ("sniper", "railgun"):
                style = "streak"
            elif variant == "smg":
                style = "needle"
        key = (size, color, style)
        if key not in self._tex_cache:
            self._tex_cache[key] = _make_bullet_texture(size, color, style)
        self.texture = self._tex_cache[key]
        self.width = size
        self.height = size
        # trail настройки
        self.trail_color = (
            min(255, int(color[0] * 1.05)),
            min(255, int(color[1] * 1.05)),
            min(255, int(color[2] * 1.05)),
            200,
        )
        if self.damage_type == "magic":
            self.trail_color = (190, 170, 255, 220)
            self.trail_length = size * 1.8
        elif self.damage_type == "hit":
            self.trail_color = (255, 190, 140, 180)
            self.trail_length = size * 1.0
        else:
            self.trail_length = size * 1.2
        if variant in ("sniper", "railgun"):
            self.trail_length *= 1.4
        elif variant == "smg":
            self.trail_length *= 0.9

    def update(self, delta_time):
        if self.life_frames is not None:
            self.life_frames -= 1
            if self.life_frames <= 0:
                self.expired = True
                self.kill()

        self.center_x += cos(radians(self.angle)) * self.speed
        self.center_y += sin(radians(self.angle)) * -self.speed
