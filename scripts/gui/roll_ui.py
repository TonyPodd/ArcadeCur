import arcade

from config import *


class RollStamina:
    def __init__(self, player: arcade.Sprite):
        """ UI для стамины рывка """
        self.player = player
        
        self.max_time = self.player.roll_cooldown
        self.cur_time = min(self.player.roll_cooldown_timer, self.max_time)
        
        # Координаты на экране
        self.x = 50
        self.y = SCREEN_HEIGHT - 60

        # Разверы
        self.width = 300
        self.height = 10

    def update(self):
        self.cur_time = min(self.player.roll_cooldown_timer, self.max_time)

    def draw(self):
        # Красный BG
        arcade.draw_lbwh_rectangle_filled(
            self.x,
            self.y,
            self.width,
            self.height,
            arcade.color.RED
        )
        
        # жёлтая стамина
        arcade.draw_lbwh_rectangle_filled(
            self.x,
            self.y,
            self.width / self.max_time * self.cur_time,
            self.height,
            arcade.color.YELLOW
        )