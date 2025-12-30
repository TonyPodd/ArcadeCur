"""
Система физики и коллизий
"""
import arcade


class PhysicsSystem:
    """Управление физикой и коллизиями"""

    def __init__(self, player: arcade.Sprite, wall_list: arcade.SpriteList):
        """
        Инициализация физической системы
        """
        self.player = player
        self.wall_list = wall_list

        # Создание физического движка arcade
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            self.wall_list
        )

    def update(self):
        """Обновление физики"""
        self.physics_engine.update()

    def add_wall(self, wall):
        """Добавление стены в физическую систему"""
        self.wall_list.append(wall)

    def check_collision(self, sprite, sprite_list):
        """
        Проверка столкновения спрайта со списком спрайтов

        Args:
            sprite: Спрайт для проверки
            sprite_list: Список спрайтов

        Returns:
            Список спрайтов, с которыми произошло столкновение
        """
        return arcade.check_for_collision_with_list(sprite, sprite_list)
