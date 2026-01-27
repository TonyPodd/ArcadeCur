import arcade
import random
import csv

from config import *
from entities import Door, Wall, Floor

class Room:
    def __init__(self, room_type: str, room_number: int, x: int, y: int, rooms_coords: tuple[tuple]):
        # settigns
        self.x = x
        self.y = y
        self.room_type = room_type
        self.room_number = room_number
        self.room_coords = rooms_coords
        
        # Sprites
        self.all_sprites = {
            'floor': arcade.SpriteList(),
            'wall': arcade.SpriteList(),
            'door': arcade.SpriteList()
        }

        # Карта комнаты
        self.text_map = list()

        # карту (пока только для 2x2 и 1x1)
        if len(rooms_coords) == 1:
            self.text_map.append(self.room_coords)
        if len(rooms_coords) == 4:
            for i in range(4):
                if i % 2 == 0:
                    self.text_map.append(list())
                self.text_map[i // 2].append(rooms_coords[i])

        # Загрузка угловых стен в чанка
        self.create_corner_walls()

    def get_sprites(self):
        """ Получить все спрайты с комнаты """
        return self.all_sprites

    def create_door(self, x: int, y: int, dir: str) -> None:
        """
        Создание двери в определённом чанке и с определённой стороны\n
        x, y - координаты чанка\n
        dir - с какой стороны будет дверь\n
        """
        # координаты первого тайла в чанке
        tile_x = x * CHUNCK_SIZE[0] * TILE_SIZE
        tile_y = y * CHUNCK_SIZE[1] * TILE_SIZE
        door_lenth = 4  # Кол-во тайлов с дверью

        # Сдвиги координат начального тайла
        if dir == 'right':
            tile_x += (CHUNCK_SIZE[0] - 1) * TILE_SIZE
        if dir == 'up':
            tile_y += (CHUNCK_SIZE[1] - 1) * TILE_SIZE

        # создание двери справа/слева
        if dir in ['right', 'left']:
            wall_lenth = (CHUNCK_SIZE[1] - 2 - door_lenth) // 2  # кол-во тайлов со стеной / 2
            
            # нижняя стена
            for i in range(wall_lenth):
                tile_y += TILE_SIZE
                self.all_sprites['wall'].append(Wall(
                    None, 1, tile_x, tile_y
                ))

            # дверь
            for i in range(door_lenth):
                tile_y += TILE_SIZE
                self.all_sprites['door'].append(Door(
                    1, tile_x, tile_y
                ))
            
            # верхняя стена
            for i in range(wall_lenth + door_lenth, CHUNCK_SIZE[1] - 2):
                tile_y += TILE_SIZE
                self.all_sprites['wall'].append(Wall(
                    None, 1, tile_x, tile_y
                ))

        # создание двери сверху/снизу
        if dir in ['up', 'down']:
            wall_lenth = (CHUNCK_SIZE[0] - 2 - door_lenth) // 2  # кол-во тайлов со стеной / 2
            
            # левая стена
            for i in range(wall_lenth):
                tile_x += TILE_SIZE
                self.all_sprites['wall'].append(Wall(
                    None, 1, tile_x, tile_y
                ))

            # дверь
            for i in range(door_lenth):
                tile_x += TILE_SIZE
                self.all_sprites['door'].append(Door(
                    1, tile_x, tile_y
                ))
            
            # правая стена
            for i in range(wall_lenth + door_lenth, CHUNCK_SIZE[1] - 2):
                tile_x += TILE_SIZE
                self.all_sprites['wall'].append(Wall(
                    None, 1, tile_x, tile_y
                ))

    def create_corner_walls(self):
        """ Создание стен по углам чанка """

        for y in range(len(self.text_map)):
            for x in range(len(self.text_map[y])):
                
                # down
                if y == 0:
                    wall_x = self.text_map[y][x][0] * CHUNCK_SIZE[0] * TILE_SIZE
                    wall_y = self.text_map[y][x][1] * CHUNCK_SIZE[1] * TILE_SIZE

                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y
                    ))
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x + TILE_SIZE * (CHUNCK_SIZE[0] - 1), wall_y
                    ))

                # up
                if y == len(self.text_map) - 1:
                    wall_x = self.text_map[y][x][0] * CHUNCK_SIZE[0] * TILE_SIZE
                    wall_y = self.text_map[y][x][1] * CHUNCK_SIZE[1] * TILE_SIZE + TILE_SIZE * (CHUNCK_SIZE[1] - 1)
                    
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y
                    ))
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x + TILE_SIZE * (CHUNCK_SIZE[0] - 1), wall_y
                    ))

                # left
                if x == 0:
                    wall_x = self.text_map[y][x][0] * CHUNCK_SIZE[0] * TILE_SIZE
                    wall_y = self.text_map[y][x][1] * CHUNCK_SIZE[1] * TILE_SIZE
                    
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y
                    ))
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y + TILE_SIZE * (CHUNCK_SIZE[1] - 1)
                    ))

                # right
                if x == len(self.text_map[y]) - 1:
                    wall_x = self.text_map[y][x][0] * CHUNCK_SIZE[0] * TILE_SIZE + (CHUNCK_SIZE[0] - 1) * TILE_SIZE
                    wall_y = self.text_map[y][x][1] * CHUNCK_SIZE[1] * TILE_SIZE
                    
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y
                    ))
                    self.all_sprites['wall'].append(Wall(
                        None, 1, wall_x, wall_y + TILE_SIZE * (CHUNCK_SIZE[1] - 1)
                    ))

    def create_wall(self, x: int, y: int, dir: str) -> None:
        """
        Функция создание стены в чанке с определнной стороны\n
        x, y - координаты чанка\n
        dir - сторона, с которой будет стоять стена
        """
        
        # координаты первого тайла в чанке
        tile_x = x * CHUNCK_SIZE[0] * TILE_SIZE
        tile_y = y * CHUNCK_SIZE[1] * TILE_SIZE

        # Сдвиги координат начального тайла
        if dir == 'right':
            tile_x += (CHUNCK_SIZE[0] - 1) * TILE_SIZE
        if dir == 'up':
            tile_y += (CHUNCK_SIZE[1] - 1) * TILE_SIZE

        if dir in ['right', 'left']:
            for i in range(CHUNCK_SIZE[1] - 2):
                tile_y += TILE_SIZE
                self.all_sprites['wall'].append(Wall(
                    None, 1, tile_x, tile_y
                ))
        
        if dir in ['up', 'down']:
            for j in range(CHUNCK_SIZE[0] - 2):
                tile_x += TILE_SIZE
                self.all_sprites['wall'].append(Wall(
                    None, 1, tile_x, tile_y
                ))

    def data_from_file(self, room_type: str) -> dict:
        """
        Загрузка объектов с файла комнаты\n
        room_type - тип комнаты
        """
        
        # Загрузить случайную комнату
        file_name = f'levels/{room_type}/{random.choice(ROOM_FILE_NAMES[room_type])}'
        with open(file=file_name, mode='r', encoding='UTF-8') as file:
            reader = csv.reader(file, delimiter=',')
            data = list(reader)
        
        all_objects = dict()  # объекты 1: (x, y)

        for i in range(len(data)):
            for j in range(len(data[i])):
                object_type = data[i][j]
                
                if object_type != '0':
                    if object_type not in all_objects:
                        all_objects[object_type] = list()
                    
                    all_objects[object_type].append((j, i))
        
        return all_objects
    
    def load_sprites_from_data(self, data: dict) -> dict:
        sprites = {
            'floor': arcade.SpriteList(),
            'wall': arcade.SpriteList(), 
        }
        
        for object_type in data:
            for j, i in data[object_type]:
                tile_x = self.x * CHUNCK_SIZE[0] * TILE_SIZE + TILE_SIZE * (j + 1)
                tile_y = self.y * CHUNCK_SIZE[1] * TILE_SIZE + TILE_SIZE * (i + 1)
            
                if object_type == '1':
                    sprites['floor'].append(Floor(
                        None, 1, tile_x, tile_y
                    ))
                    
                if object_type == '2':
                    sprites['wall'].append(Wall(
                        None, 1, tile_x, tile_y
                    ))

        return sprites
    
    def add_new_sprites(self, sprites: dict) -> None:
        """
        Добавление новых спрайтов\n
        sprites - словарь с новыми спрайтами
        """
        for sprite_name in sprites:
            sprite_list = sprites[sprite_name].sprite_list
            
            for sprite in sprite_list:
                if sprite_name not in self.all_sprites:
                    self.all_sprites[sprite_name] = arcade.SpriteList()
                self.all_sprites[sprite_name].append(sprite)