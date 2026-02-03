import arcade
import random

import config


class GameCamera:
    """Камера для следования за игроком"""

    def __init__(self) -> None:
        self.camera = arcade.camera.Camera2D()
        self.viewport_margin = config.VIEWPORT_MARGIN
        self._shake_timer = 0.0
        self._shake_duration = 0.0
        self._shake_intensity = 0.0
        self._shake_offset = (0.0, 0.0)

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
        # Применяем тряску
        if self._shake_timer > 0:
            self.camera.position = (
                self.camera.position[0] + self._shake_offset[0],
                self.camera.position[1] + self._shake_offset[1],
            )

    def get_position(self):
        return self.camera.position

    def update(self, delta_time: float) -> None:
        if self._shake_timer <= 0:
            self._shake_offset = (0.0, 0.0)
            return

        self._shake_timer = max(0.0, self._shake_timer - delta_time)
        t = self._shake_timer / self._shake_duration if self._shake_duration > 0 else 0.0
        strength = self._shake_intensity * t
        self._shake_offset = (
            random.uniform(-strength, strength) if strength > 0 else 0.0,
            random.uniform(-strength, strength) if strength > 0 else 0.0,
        )

    def shake(self, intensity=10, duration=0.2):
        self._shake_intensity = max(self._shake_intensity, intensity)
        self._shake_duration = max(self._shake_duration, duration)
        self._shake_timer = max(self._shake_timer, duration)

    def zoom(self, zoom_level):
        # TODO: Реализовать масштабирование
        ...

    def set_position(self, x, y):
        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            (x, y),
            1
        )
