import arcade
import csv
import random

from entities import Wall, Floor
from levels import Room
from config import *

class Level:
    def __init__(self, level_type: str):
        self.level_type = level_type  # Тип уровня 

        # Спрайты всех объектов комнаты
        self.all_sprites = dict()

        # Карта чанков
        self.text_map = list()
        for i in range(CHUNCK_SIZE[1]):
            self.text_map.append(list())
            for j in range(CHUNCK_SIZE[0]):
                self.text_map[i].append(0)
                # 0 - Пустой чанк

        self.rooms = dict()    # Все комнаты
        self.current_room = 1  # номер текущей комнаты
        self.room_path = dict()
        self.number_of_rooms = {  # количество комнат определённого типа
            'fight': 0,
            'loot': 0,
            'shop': 0
        }

        # Загрузка других комнат
        self.load_rooms()
        # Загрузка стен и дверей
        self.load_walls_and_doors()
        # Загрузка спрайтов с комнат
        self.load_sprites()

    def load_rooms(self):
        """ Функция случайной загруски комнат """

        # Стартовая комната (лифт)
        x, y = random.randint(0, LEVEL_SIZE[0] - 1), random.randint(0, LEVEL_SIZE[1] - 1)
        self.create_room(
            'spawn',
            self.current_room,
            x, y
        )
        self.room_path[self.current_room] = list()
        self.current_room += 1
        
        # Выбираем положение комнат чанков
        for i in range(random.randint(6, 11)):
            x, y, possible_directions = self.choose_dir(x, y)  # Ищем новый путь для комнаты
            dir = random.choice(possible_directions)  # выбираем, в каком направление будет следующая комната
            room_num_from = self.text_map[y][x]  # номер комнаты из которой будем переходить в следующую

            # Определяем тип комнаты
            if self.number_of_rooms['loot'] == self.number_of_rooms['fight'] or self.number_of_rooms['shop'] == self.number_of_rooms['fight']:
                room_type = 'fight'
            elif self.number_of_rooms['shop'] < 1:
                room_type = random.choice(['fight', 'loot', 'shop'])
            else:
                room_type = random.choice(['fight', 'loot'])
            self.number_of_rooms[room_type] += 1
            
            self.create_room(
                room_type,
                self.current_room,
                x, y,
                room_num_from,
                dir
            )

            self.current_room += 1  # новый номер для ледующей комнаты
        
        print('Комнаты загружены\n')

    def create_room(
        self,
        room_type: str,
        current_room_number: int,
        x_from: int,
        y_from: int,
        room_number_from: int=None,
        direction: str=None
        ) -> None:
        """
        Создание комнаты\n
        room_type - тип комнаты(fight/loot/shop/boss/spawn) \n
        room_number - номер комнаты \n
        x_from, y_from - координаты комнаты, из которой создаётся новая, на карте чанков\n
        room_number_from - номер комнаты, из которой создаётся новая\n
        direction - в какую сторону будет создаваться комната\n
        """

        # Для создания лифта
        if room_type == 'spawn':
            self.rooms[current_room_number] = Room(
                room_type,
                current_room_number,
                x_from, y_from,
                ((x_from, y_from))
            )
            self.text_map[y_from][x_from] = current_room_number
            self.room_path[current_room_number] = list()

        # остольные комнаты
        else:
            # Устанавлеваем координаты новой комнаты и указываем, где будет дверь в этой комнате
            if direction == 'left':
                next_x, next_y = x_from - 1, y_from
                self.room_path[current_room_number] = [(next_x, next_y, 'right')]
                self.room_path[room_number_from].append((x_from, y_from, 'left'))

            if direction == 'right':
                next_x, next_y = x_from + 1, y_from
                self.room_path[current_room_number] = [(next_x, next_y, 'left')]
                self.room_path[room_number_from].append((x_from, y_from, 'right'))

            if direction == 'up':
                next_x, next_y = x_from, y_from - 1
                self.room_path[current_room_number] = [(next_x, next_y, 'down')]
                self.room_path[room_number_from].append((x_from, y_from, 'up'))

            if direction == 'down':
                next_x, next_y = x_from, y_from + 1
                self.room_path[current_room_number] = [(next_x, next_y, 'up')]
                self.room_path[room_number_from].append((x_from, y_from, 'down'))
            
            # размер комнаты
            if room_type == 'shop' or room_type == 'loot':
                size = ([(next_x, next_y)])
            else:
                size = random.choice(self.check_room_size(next_x, next_y))
            
            # Заполнение чанков
            for coords in size:
                x, y = coords[0], coords[1]
                self.text_map[y][x] = current_room_number

            # Создание комнаты
            self.rooms[current_room_number] = Room(
                room_type, current_room_number, next_x, next_y, size
            )
        
        print(f'Создана комната №{current_room_number}\n')

    def check_room_size(self, x: int, y: int) -> list[list[tuple]]:
        """
        Проверка: какие размеры комнаты могут быть
        """

        output = [[(x, y)]]

        # 2x2 варианты
        for i in range(2):
            for j in range(2):
                x1, x2, x3, x4 = x - 1 + j, x + j, x - 1 + j, x + j
                y1, y2, y3, y4 = y - 1 + i, y - 1 + i, y + i, y + i
                if x1 >= 0 and x2 < LEVEL_SIZE[0] and y3 >= 0 and y4 < LEVEL_SIZE[1]:
                    if self.text_map[y1][x1] == 0 and self.text_map[y2][x2] == 0 and self.text_map[y3][x3] == 0 and self.text_map[y4][x4] == 0:
                        output.append([(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
        return output

    def choose_dir(self, x: int, y: int) -> tuple[int, int, list]:
        """ Выбор случайного направления """

        possible_directions = list()

        # left
        if self.text_map[y][x - 1] == 0 and x - 1 >= 0:
            possible_directions.append('left')

        # right
        if self.text_map[y][x + 1] == 0 and x + 1 < LEVEL_SIZE[0]:
            possible_directions.append('right')

        # up
        if self.text_map[y - 1][x] == 0 and y - 1 >= 0:
            possible_directions.append('up')

        # down
        if self.text_map[y + 1][x] == 0 and y + 1 < LEVEL_SIZE[1]:
            possible_directions.append('down')

        if possible_directions:
            return (x, y, possible_directions)

        while True:
            x, y = random.randint(0, LEVEL_SIZE[0] - 1), random.randint(0, LEVEL_SIZE[1] - 1)
            if self.text_map[y][x] != 0:
                return self.choose_dir(
                    x, y
                )

    def load_walls_and_doors(self) -> None:
        for y in range(LEVEL_SIZE[1]):
            for x in range(LEVEL_SIZE[0]):
                if self.text_map[y][x] != 0:
                    current_room_number = self.text_map[y][x]
                    pathes = self.room_path[current_room_number]  # расположение дверей
                    room = self.rooms[current_room_number]

                    # left
                    if x - 1 >= 0:
                        dx = x - 1
                        dy = y
                        dir = 'left'

                        if (dx, dy, dir) not in pathes and self.text_map[dy][dx] != current_room_number:
                            room.create_wall(dx, dy, dir)
                        elif (dx, dy, dir) not in pathes:
                            room.create_door(dx, dy, dir)
                    
                    # right
                    if x + 1 < LEVEL_SIZE[0]:
                        dx = x + 1
                        dy = y
                        dir = 'right'
                        
                        if (dx, dy, dir) not in pathes and self.text_map[dy][dx] != current_room_number:
                            room.create_wall(dx, dy, dir)
                        elif (dx, dy, dir) not in pathes:
                            room.create_door(dx, dy, dir)
                    
                    # up
                    if y - 1 >= 0:
                        dy = y - 1
                        dx = x
                        dir = 'up'
                        
                        if (dx, dy, dir) not in pathes and self.text_map[dy][dx] != current_room_number:
                            room.create_wall(dx, dy, dir)
                        elif (dx, dy, dir) not in pathes:
                            room.create_door(dx, dy, dir)
                    
                    # down
                    if y + 1 < LEVEL_SIZE[1]:
                        dy = y - 1
                        dx = x
                        dir = 'down'
                        
                        if (dx, dy, dir) not in pathes and self.text_map[dy][dx] != current_room_number:
                            room.create_wall(dx, dy, dir)
                        elif (dx, dy, dir) not in pathes:
                            room.create_door(dx, dy, dir)

        print('Загрузка дверей и стен закончилась\n')

    def load_sprites(self):
        for room_num in self.rooms:
            room_sprites = self.rooms[room_num].get_sprites()
            for key in room_sprites:
                if key not in self.all_sprites:
                    self.all_sprites[key] = room_sprites[key]
                else:
                    for sprite in room_sprites[key].sprite_list:
                        self.all_sprites[key].append(sprite)
        print('Спрайты с комнат загружены\n')

    def get_sprites(self):
        return self.all_sprites
