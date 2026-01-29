import arcade
from math import cos, sin, radians
from config import *

class Bullet(arcade.Sprite):
    def __init__(self, scale=1, center_x=0, center_y=0):
        super().__init__(":resources:/images/space_shooter/laserBlue01.png", scale, center_x, center_y)

        self.speed = DEFAULT_BULLET_VELOCITY
        self.angle = 0
        self.damage = 0
        self.damage_type = ""
        self.bullet_radius = 0
        self.bullet_speed = 0

    def apply_stats(self):
        if self.bullet_speed:
            self.speed = self.bullet_speed
        if self.bullet_radius:
            size = self.bullet_radius * 2
            self.width = size
            self.height = size

    def update(self):
        self.center_x += cos(radians(self.angle)) * self.speed
        self.center_y += sin(radians(self.angle)) * -self.speed
