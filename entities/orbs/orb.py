import arcade
import random
import math


class Orb(arcade.Sprite):
    def __init__(self, path_or_texture=None, scale=1, center_x=0, center_y=0):
        """
        Орб, который Выпадает с врагов \n
        Нужен для перехода между локациями
        """
        super().__init__(path_or_texture, scale, center_x, center_y)

        self.value = random.randint(1, 10)  # сколько даётся с одного орба такого
        self.player_nearby = False  # Есть ли игрок рядом
        self.speed = 10
        self.radius = 200
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

