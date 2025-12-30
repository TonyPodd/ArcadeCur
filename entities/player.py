import arcade

import config


class Player(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()

        # Временный квадрат вместо спрайта
        self.texture = arcade.make_soft_square_texture(40, arcade.color.BLUE, outer_alpha=255)

        self.center_x = x
        self.center_y = y

        self.max_speed = config.PLAYER_MOVEMENT_SPEED
        self.acceleration = config.PLAYER_ACCELERATION
        self.friction = config.PLAYER_FRICTION

        # Направление движения
        self.direction = {
            'left': False,
            'right': False,
            'up': False,
            'down': False
        }

    def update(self) -> None:
        
        if self.direction['left']:
            move_direction_x = -1
        elif self.direction['right']:
            move_direction_x = 1
        else:
            move_direction_x = 0

        if self.direction['down']:
            move_direction_y = -1
        elif self.direction['up']:
            move_direction_y = 1
        else:
            move_direction_y = 0

        # Применяем ускорение в направлении движения
        if move_direction_x != 0:
            self.change_x += move_direction_x * self.acceleration
        else:
            # Применяем трение когда нет ввода
            self.change_x *= (1 - self.friction)

        if move_direction_y != 0:
            self.change_y += move_direction_y * self.acceleration
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
