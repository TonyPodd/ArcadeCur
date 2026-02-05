import arcade
import random
import csv
from pathlib import Path

from .room import Room
from entities import Enemy, Wall, Floor
from config import *


class FightRoom(Room):
    def __init__(self, room_type, room_number, x, y, rooms_coords, difficulty):
        super().__init__(room_type, room_number, x, y, rooms_coords, difficulty)

        self.data = self.data_from_file(self.room_type)
        sprites_from_data = self.load_sprites_from_data(self.data)
        self.add_new_sprites(sprites_from_data)

        self.status = 0  # статус комнаты: 0 - не зачищена, 1 - зачищена

    def data_from_file(self, room_type: str) -> dict:
        """
        Загрузка объектов с файла комнаты\n
        room_type - тип комнаты
        """
        n = len(self.text_map)
        # Загрузить случайную комнату
        size_key = f"{n}x{n}"
        file_name = f"levels/{room_type}/{size_key}/{random.choice(ROOM_FILE_NAMES[room_type][size_key])}"
        file_path = Path(__file__).resolve().parent.parent / file_name
        with open(file=file_path, mode='r', encoding='UTF-8') as file:
            reader = csv.reader(file, delimiter=',')
            data = list(reader)[::-1]

        all_objects = dict()  # объекты 1: (x, y)

        for i in range(len(data)):
            for j in range(len(data[i])):
                object_type = data[i][j]

                if object_type != '0':
                    if object_type not in all_objects:
                        all_objects[object_type] = list()

                    all_objects[object_type].append((j, i))

        return all_objects

    def begin_fight(self):
        self.close_doors()
        return self.valid_spawn_tiles()

    def end_fight(self):
        self.status = 1
        self.open_doors()

    def spawn_enemies(self, valid_tiles_sprites: arcade.SpriteList) -> arcade.SpriteList:
        """
        Создание врагов в комнате
        """
        enemy_count = len(valid_tiles_sprites.sprite_list)
        
        if 'enemy' not in self.all_sprites:
            self.all_sprites['enemy'] = arcade.SpriteList()
            
        for tile in valid_tiles_sprites:
            self.all_sprites['enemy'].append(Enemy(
                tile.center_x,
                tile.center_y,
                difficulty=self.difficulty
            ))

        return self.all_sprites['enemy']

    def valid_spawn_tiles(self) -> arcade.SpriteList:
        """ Находит все места, на которых может заспавниться враг """
        spawn_sprites = arcade.SpriteList()
        floor_sprites = self.all_sprites['floor'].sprite_list.copy()

        room_size = len(self.text_map)
        if room_size == 1:
            min_count, max_count = FIGHT_ROOM_ENEMY_COUNT_1X1
        else:
            min_count, max_count = FIGHT_ROOM_ENEMY_COUNT_2X2

        enemy_count = random.randint(min_count, max_count)
        
        for _ in range(enemy_count):
            tile = random.choice(floor_sprites)
            sprite = arcade.Sprite(
                arcade.make_circle_texture(
                    TILE_SIZE,
                    (214, 17, 60)
                ),
                1,
                tile.center_x,
                tile.center_y
            )
            spawn_sprites.append(sprite)
            floor_sprites.remove(tile)

        return spawn_sprites

    def close_doors(self):
        for door in self.all_sprites['door']:
            # закрыть дверь
            door.close_door()

    def open_doors(self):
        """
        Открытие всех дверей
        """
        for door in self.all_sprites['door']:
            door.open_door()
