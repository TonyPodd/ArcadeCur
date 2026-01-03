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

        # Направление движения
        self.direction = {
            'left': False,
            'right': False,
            'up': False,
            'down': False
        }

        # Последнее нажатое направление
        self.last_direction_x = None  # 'left' или 'right'
        self.last_direction_y = None  # 'up' или 'down'

    def update(self, delta_time: float) -> None:
        move_direction_x = 0
        if self.direction['right'] and self.direction['left']:
            # Обе клавиши нажаты - используем последнюю
            if self.last_direction_x == 'right':
                move_direction_x = 1
            elif self.last_direction_x == 'left':
                move_direction_x = -1
        elif self.direction['right']:
            move_direction_x = 1
        elif self.direction['left']:
            move_direction_x = -1

        move_direction_y = 0
        if self.direction['up'] and self.direction['down']:
            if self.last_direction_y == 'up':
                move_direction_y = 1
            elif self.last_direction_y == 'down':
                move_direction_y = -1
        elif self.direction['up']:
            move_direction_y = 1
        elif self.direction['down']:
            move_direction_y = -1

        self.change_x = move_direction_x * self.max_speed * delta_time
        self.change_y = move_direction_y * self.max_speed * delta_time

    def do_roll(self):
        pass