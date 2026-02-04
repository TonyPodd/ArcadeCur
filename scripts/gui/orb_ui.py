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

    def draw(self):
        # Задний фон
        arcade.draw_lbwh_rectangle_filled(
            SCREEN_WIDTH - self.width,
            SCREEN_HEIGHT - self.height,
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
            SCREEN_WIDTH - self.width + 60,
            SCREEN_HEIGHT - 25,
            arcade.color.WHITE,
            14
        )
        arcade.draw_text(
            str(self.money),
            SCREEN_WIDTH - self.width + 60,
            SCREEN_HEIGHT - 65,
            arcade.color.WHITE,
            14
        )