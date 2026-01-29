import arcade

import config


class Player(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()
        
        # settings
        self.player_hp = config.PLAYER_HEALTH_POINTS

        # Временный квадрат вместо спрайта
        self.texture = arcade.make_soft_square_texture(40, arcade.color.BLUE, outer_alpha=255)
        self._hit_box._points = ((-20, -15), (20, -15), (20, 15), (-20, 15))

        self.center_x = x
        self.center_y = y

        # Направление движения
        self.direction = {
            'left': False,
            'right': False,
            'up': False,
            'down': False
        }

        # Перекат
        self.is_roll = False
        self.roll_speed = config.PLAYER_ROLL_SPEED
        self.roll_timer = config.PLAYER_ROLL_TIMER
        self.roll_direction = {
            'x': 0,  # Направление переката по X
            'y': 0   # Направление переката по Y
        }

        # Последнее нажатое направление
        self.last_direction_x = None  # 'left' или 'right'
        self.last_direction_y = None  # 'up' или 'down'

        # Храним подобранные игроком предметы
        self.current_slot = 0
        self.first_item = None
        self.second_item = None

    def update(self, delta_time: float) -> None:
        move_direction_x, move_direction_y = self.move()

        # передвижение
        if not self.is_roll:
            self.change_x = move_direction_x * self.max_speed * delta_time
            self.change_y = move_direction_y * self.max_speed * delta_time

        # перекат
        elif self.is_roll:
            self.change_x = self.roll_speed * self.roll_direction['x'] * delta_time
            self.change_y = self.roll_speed * self.roll_direction['y'] * delta_time
            self.roll_timer -= delta_time

            if self.roll_direction['x'] == 1:
                self.angle += 20
            elif self.roll_direction['x'] == -1:
                self.angle -= 20
            else:
                self.angle += 20

            if self.roll_timer <= 0:
                self.roll_timer = config.PLAYER_ROLL_TIMER
                self.is_roll = False
                self.angle = 0

    def do_roll(self):
        # Определяем направление по X
        if self.direction['left']:
            self.roll_direction['x'] = -1
        elif self.direction['right']:
            self.roll_direction['x'] = 1
        else:
            self.roll_direction['x'] = 0

        # Определяем направление по Y
        if self.direction['up']:
            self.roll_direction['y'] = 1
        elif self.direction['down']:
            self.roll_direction['y'] = -1
        else:
            self.roll_direction['y'] = 0

        self.is_roll = True

    def move(self) -> tuple[int, int]:
        """ Определет направления игрока """
        move_direction_x, move_direction_y = 0, 0

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

        return (move_direction_x, move_direction_y)

    def set_position(self, x: float, y: float) -> None:
        """ Ставит новые координаты играка """
        self.center_x = x
        self.center_y = y
