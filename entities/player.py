import arcade

import config


class Player(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__()

        # settings
        self.is_dead = False  # Умер ли игрок
        self.hp = config.PLAYER_HEALTH_POINTS
        self.max_speed = config.PLAYER_MOVEMENT_SPEED
        self.view_angle = 0.0

        # Временный квадрат вместо спрайта
        self.texture = arcade.make_soft_square_texture(40, arcade.color.BLUE, outer_alpha=255)
        self._hit_box._points = ((-20, -15), (20, -15), (20, 15), (-20, 15))

        self.center_x = x
        self.center_y = y

        # Не дамажить одной пулей дважды
        self.bullets_hitted = arcade.SpriteList()

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
        self.roll_cooldown = 2  # Время, которое нужно для следующего переката
        self.roll_cooldown_timer = self.roll_cooldown # Время от прошлого переката
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
        if not self.is_dead:
            move_direction_x, move_direction_y = self.move()

            # передвижение
            if not self.is_roll:
                self.change_x = move_direction_x * self.max_speed * delta_time
                self.change_y = move_direction_y * self.max_speed * delta_time
                self.roll_cooldown_timer += delta_time

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
                    self.roll_cooldown_timer = 0.0
        else:
            self.change_x = 0
            self.change_y = 0

    def do_roll(self):
        if not self.is_dead and self.roll_cooldown_timer >= self.roll_cooldown:
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
        else:
            self.is_roll = False

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

    def take_damage(self, damage: float) -> None:
        self.hp -= damage
        if self.hp <= 0:
            self.on_die()

    def on_die(self):
        self.is_dead = True

    def draw_item(self):
        """ Отрисовывать предмет в руках """
        if not self.is_dead:
            if self.current_slot == 0:
                if self.first_item is not None:
                    self.first_item.draw()
            elif self.current_slot == 1:
                if self.second_item is not None:
                    self.second_item.draw()

    def drop_item(self) -> arcade.Sprite:
        """
        Функция для выбрасывания item в руках \n
        Если игрок умер, возвращает False\n
        Возвращает спрайт в руках и удаляет его из инвентаря\n
        """
        # Если умер
        if self.is_dead:
            return False

        # Проверяем есть ли item в слоту
        dropped_item = None
        if self.current_slot == 0 and self.first_item is not None:
            dropped_item = self.first_item
            self.first_item = None
            return dropped_item

        if self.current_slot == 1 and self.second_item is not None:
            dropped_item = self.second_item
            self.second_item = None
            return dropped_item

        return None

    def grab_item(self, item_sprite: arcade.Sprite):
        """
        Функция для добавления item в инвентарь \n
        item_sprite - спрайт, который хотим поднять \n
        Если  инвентарь переполнин, то скидываем предмет, который в руках, и поднимаем новый \n
        Возвращаем True/False/Sprite:\n
        Если есть свободые слоты, то True \n
        Если персонаж умер, то False\n
        Елси нет свободных слотов, то Sprite
        """
        # Умер
        if self.is_dead:
            return False

        # Проверка свободных слотов
        if self.first_item is None:
            self.first_item = item_sprite
            self.current_slot = 0
            return True
        elif self.second_item is None:
            self.second_item = item_sprite
            self.current_slot = 1
            return True

        # Нет свободных слотов
        elif self.current_slot == 0:
            dropped_item = self.drop_item()
            self.first_item = item_sprite
            return dropped_item
        elif self.current_slot == 1:
            dropped_item = self.drop_item()
            self.second_item = item_sprite
            return dropped_item

    def get_items_texture(self) -> list[arcade.Sprite, arcade.Sprite]:
        """
        Возвращает массив спрайтов с текстураим item'ов \n
        """
        try:
            first_texture = self.first_item.get_texture()
        except Exception:
            first_texture = None
        try:
            second_texture = self.second_item.get_texture()
        except Exception:
            second_texture = None

        return [first_texture, second_texture]
