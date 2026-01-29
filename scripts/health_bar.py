import arcade

from config import *


class HealthBar:
    def __init__(self, player: arcade.sprite) -> None:
        # settigns
        self.speed = 100 # скорость для анимации
        self.player = player

        # Координаты на экране
        self.x = 50
        self.y = SCREEN_HEIGHT - 50

        # Разверы
        self.width = 300
        self.height = 20

        # hp
        self.max_hp = PLAYER_HEALTH_POINTS
        self.current_hp = self.max_hp  # HP игрока в данный момент
        self.display_hp = self.max_hp  # HP которое отображается
    
    def draw(self) -> None:
        # Красный BG
        arcade.draw_lbwh_rectangle_filled(
            self.x,
            self.y,
            self.width,
            self.height,
            arcade.color.RED
        )
        
        # Зелёные current hp
        arcade.draw_lbwh_rectangle_filled(
            self.x,
            self.y,
            self.width / self.max_hp * self.display_hp,
            self.height,
            arcade.color.GREEN
        )
        
        # Каёмка
        arcade.draw_lbwh_rectangle_outline(
            self.x,
            self.y,
            self.width,
            self.height,
            (0, 0, 0),
            5
        )

    def update(self, delta_time: float= 1 / 60) -> None:
        self.current_hp = self.player.player_hp
        
        if self.display_hp > self.current_hp:
            self.display_hp -= self.speed * delta_time
        
        if self.display_hp - self.current_hp <= 0.1:
            self.display_hp = self.current_hp
        
        if self.display_hp <= 0:
            self.display_hp = 0
