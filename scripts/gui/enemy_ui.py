import arcade

from config import *


class EnemyUi:
    def __init__(self):
        """ Отриковта количества врагов """
        self.max_enemy = 0
        self.cur_enemy = 0
        
        self.width = 100
        self.height = 60
        
        self.x = (SCREEN_WIDTH - self.width) / 2
        self.y = 60
        
        self.text_color = (217, 47, 4)

    def update(self, remaining_enemies: int):
        self.cur_enemy = remaining_enemies

    def set_num_of_enemy(self, max_enemy: int):
        """ Новое максимально кол-во врагов в комнате """
        self.max_enemy = max_enemy

    def draw(self):
        # BG
        arcade.draw_lbwh_rectangle_filled(
            self.x,
            self.y,
            self.width,
            self.height,
            (90, 90, 90, 150)
        )
        
        # text
        arcade.draw_text(
            'Enemies',
            self.x + 5,
            self.y + self.height - 23,
            self.text_color,
            20
        )
        # кол-во врагов
        arcade.draw_text(
            f'{self.cur_enemy}/{self.max_enemy}',
            self.x + 25,
            self.y + self.height - 46,
            self.text_color,
            20
        )