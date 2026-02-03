import arcade
import random
import math

from config import *


class Orb(arcade.Sprite):
    def __init__(self, path_or_texture=None, scale=1, center_x=0, center_y=0):
        """
        Орб, который Выпадает с врагов \n
        Нужен для перехода между локациями
        """
        super().__init__(path_or_texture, scale, center_x, center_y)

        self.value = random.randint(1, 10)  # сколько даётся с одного орба такого
        self.player_nearby = False  # Есть ли игрок рядом
        self.speed = ABSORPTION_SPEED
        self.radius = ABSORPTION_RADIUS
        self.trigger = arcade.SpriteCircle(
            self.radius,
            arcade.color.AERO_BLUE,
            False,
            self.center_x,
            self.center_y
        )

        self.resize()

    def picked_up(self):
        """ Орб подобран """
        self.kill()
        return self.value

    def resize(self):
        """
        Размер относительно стоимости
        """
        self.width = 20 + 2 * (self.value - 1)
        self.height = 20 + 2 * (self.value - 1)
        self.texture = arcade.make_soft_circle_texture(self.width, (34, 188, 240))

    def absorption(self):
        # Создание единичного вектора e. L - квадрат расстояния между игроком и орбой

        L = (self.player_x - self.center_x) ** 2 + (self.player_y - self.center_y) ** 2
        e = ((self.player_x - self.center_x) / L ** 0.5, (self.player_y - self.center_y) / L ** 0.5)

        if self.radius ** 2 >= L:
            self.center_x += self.speed * e[0]
            self.center_y += self.speed * e[1]

    def update(self, delta_time: float = 1 / 60, *args) -> None:
        args = list(args)
        self.player_x = args[0][0]
        self.player_y = args[0][1]

        self.absorption()
        

