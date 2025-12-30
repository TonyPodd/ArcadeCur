import arcade

import config


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Временный квадрат вместо спрайта
        self.texture = arcade.make_soft_square_texture(40, arcade.color.BLUE, outer_alpha=255)

        self.center_x = x
        self.center_y = y

        self.max_speed = config.PLAYER_MOVEMENT_SPEED
        self.acceleration = config.PLAYER_ACCELERATION
        self.friction = config.PLAYER_FRICTION

        # Направление движения
        self.move_direction_x = 0
        self.move_direction_y = 0

    def update(self):
        # Применяем ускорение в направлении движения
        if self.move_direction_x != 0:
            self.change_x += self.move_direction_x * self.acceleration
        else:
            # Применяем трение когда нет ввода
            self.change_x *= (1 - self.friction)

        if self.move_direction_y != 0:
            self.change_y += self.move_direction_y * self.acceleration
        else:
            # Применяем трение когда нет ввода
            self.change_y *= (1 - self.friction)

        # Ограничиваем максимальную скорость
        if abs(self.change_x) > self.max_speed:
            self.change_x = self.max_speed if self.change_x > 0 else -self.max_speed
        if abs(self.change_y) > self.max_speed:
            self.change_y = self.max_speed if self.change_y > 0 else -self.max_speed

        # Останавливаем полностью если скорость очень маленькая
        if abs(self.change_x) < 0.1:
            self.change_x = 0
        if abs(self.change_y) < 0.1:
            self.change_y = 0

        # Позиция обновляется PhysicsEngine
