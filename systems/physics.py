"""
Система физики и коллизий
"""
import arcade


class PhysicsSystem:
    """Управление физикой и коллизиями"""

    def __init__(self, player: arcade.Sprite, wall_list: arcade.SpriteList):
        self.player = player
        self.wall_list = wall_list

        # Создание физического движка arcade
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            self.wall_list
        )

    def update(self) -> None:
        self.physics_engine.update()

    def add_wall(self, wall: arcade.Sprite) -> None:
        self.wall_list.append(wall)

    def check_collision(self, sprite: arcade.Sprite, sprite_list:arcade.SpriteList) -> list[arcade.Sprite]:
        """
        Проверка столкновения спрайта со списком спрайтов
        """
        return arcade.check_for_collision_with_list(sprite, sprite_list)
