import arcade

from config import *


class EnemyUi:
    def __init__(self):
        """ Отриковта количества врагов """
        self.max_enemy = 0
        self.cur_enemy = 0

    def update(self, remaining_enemies: int):
        self.cur_enemy = remaining_enemies

    def set_num_of_enemy(self, max_enemy: int):
        """ Новое максимально кол-во врагов в комнате """
        self.max_enemy = max_enemy

    def draw(self):
        ...