import arcade

import config


class GameCamera:
    """Камера для следования за игроком"""

    def __init__(self) -> None:
        self.camera = arcade.camera.Camera2D()
        self.viewport_margin = config.VIEWPORT_MARGIN

    def use(self) -> None:
        self.camera.use()

    def center_on_sprite(self, sprite: arcade.Sprite, speed: float=0.1) -> None:
        target_position = (sprite.center_x, sprite.center_y)

        # Перемещаем камеру к позиции спрайта
        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            target_position,
            speed
        )

    def get_position(self):
        return self.camera.position

    def shake(self, intensity=10):
        # TODO: Реализовать эффект тряски
        ...

    def zoom(self, zoom_level):
        # TODO: Реализовать масштабирование
        ...

    def set_position(self, x, y):
        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            (x, y),
            1
        )