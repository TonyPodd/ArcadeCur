import arcade
import random
import csv
from pathlib import Path

from .room import Room
from entities.enemy import Enemy
from config import *


class FightRoom(Room):
    def __init__(self, room_type, room_number, x, y, rooms_coords):
        super().__init__(room_type, room_number, x, y, rooms_coords)

        data = self.data_from_file(self.room_type)
        sprites_from_data = self.load_sprites_from_data(data)
        self.add_new_sprites(sprites_from_data)
        self.create_enemies_from_data(data)

    def create_enemies_from_data(self, data):
        wall_tiles = set(data.get('2', []))
        floor_tiles = set(data.get('1', []))

        def is_clear(tile):
            if tile not in floor_tiles:
                return False
            x, y = tile
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for n in neighbors:
                if n in wall_tiles:
                    return False
            return True

        valid_tiles = [t for t in floor_tiles if is_clear(t)]
        if not valid_tiles:
            return

        room_size = len(self.text_map)
        if room_size == 1:
            min_count, max_count = FIGHT_ROOM_ENEMY_COUNT_1X1
        else:
            min_count, max_count = FIGHT_ROOM_ENEMY_COUNT_2X2
            
        enemy_count = random.randint(min_count, max_count)
        enemy_count = min(enemy_count, len(valid_tiles))

        if 'enemy' not in self.all_sprites:
            self.all_sprites['enemy'] = arcade.SpriteList()

        used = set()
        for _ in range(enemy_count):
            tile = random.choice(valid_tiles)
            while tile in used and len(used) < len(valid_tiles):
                tile = random.choice(valid_tiles)
            used.add(tile)

            tile_x, tile_y = tile
            center_x = self.x * CHUNCK_SIZE[0] * TILE_SIZE + TILE_SIZE * (tile_x + 1)
            center_y = self.y * CHUNCK_SIZE[1] * TILE_SIZE + TILE_SIZE * (tile_y + 1)
            self.all_sprites['enemy'].append(Enemy(center_x, center_y))

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
