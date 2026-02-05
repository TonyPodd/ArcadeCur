import arcade

from config import *


class OrbUi:
    def __init__(self):
        """ Интерфейс для понимания сколько денег и орбов у игрока """
        self.orbs = 0
        self.money = 0
        
        self.width = 150
        self.height = 100
        
        self.orb_texture = arcade.Sprite(
            arcade.make_soft_circle_texture(
                30, (34, 188, 240)
            ),
            1,
            SCREEN_WIDTH - self.width + 20,
            SCREEN_HEIGHT - 20
        )
        self.money_texture = arcade.Sprite(
            arcade.make_soft_circle_texture(
                30, (245, 200, 2)
            ),
            1,
            SCREEN_WIDTH - self.width + 20,
            SCREEN_HEIGHT - 60
        )
        
    def update(self, orbs: int, money: int):
        self.orbs = orbs
        self.money = money

    def draw(self, screen_width, screen_height):
        self.orb_texture.center_x = screen_width - self.width + 20
        self.orb_texture.center_y = screen_height - 20
        
        self.money_texture.center_x = screen_width - self.width + 20
        self.money_texture.center_y = screen_height - 60
        # Задний фон
        arcade.draw_lbwh_rectangle_filled(
            screen_width - self.width,
            screen_height - self.height,
            self.width,
            self.height,
            (90, 90, 90, 150)
        )
        
        # отрисока текстур орбов
        arcade.draw_sprite(self.orb_texture)
        arcade.draw_sprite(self.money_texture)
        
        # Количество орбов
        arcade.draw_text(
            str(self.orbs),
            screen_width - self.width + 60,
            screen_height - 25,
            arcade.color.WHITE,
            14
        )
        arcade.draw_text(
            str(self.money),
            screen_width - self.width + 60,
            screen_height - 65,
            arcade.color.WHITE,
            14
        )