import arcade

import config


class GameCamera:
    """Камера для следования за игроком"""

    def __init__(self, width, height):
        self.camera = arcade.camera.Camera2D()
        self.viewport_margin = config.VIEWPORT_MARGIN

    def use(self):
        self.camera.use()

    def center_on_sprite(self, sprite, speed=0.1):
        target_position = (sprite.center_x, sprite.center_y)
        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            target_position,
            speed
        )

    def move_to(self, position, speed=0.1):
        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            position,
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
