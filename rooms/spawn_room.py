import arcade
import random

from .room import Room
from config import *
from entities import Floor, Wall, Chest, InetactiveObject


class SpawnRoom(Room):
    def __init__(self, room_type, room_number, x, y, rooms_coords):
        super().__init__(room_type, room_number, x, y, rooms_coords)
        self.create_spawn()

        data = self.data_from_file('spawn')
        sprites_from_data = self.load_sprites_from_data(data)
        self.add_new_sprites(sprites_from_data)
        self.create_chests_from_data(data)

    def create_spawn(self) -> None:
        spawn_x = self.x * CHUNCK_SIZE[0] * TILE_SIZE + (CHUNCK_SIZE[0] * TILE_SIZE) // 2
        spawn_y = self.y * CHUNCK_SIZE[1] * TILE_SIZE + (CHUNCK_SIZE[1] * TILE_SIZE) // 2
        self.spawn = Floor(None, 1, spawn_x, spawn_y)

    def get_spawn(self) -> arcade.Sprite:
        return self.spawn

    def create_chests_from_data(self, data) -> None:
        # Гарантированный спавн 3 сундуков в стартовой комнате
        wall_tiles = set(data.get('2', []))
        floor_tiles = set(data.get('1', []))

        def is_clear(tile):
            if tile not in floor_tiles:
                return False
            x, y = tile
            # не рядом со стеной (4-соседа)
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for n in neighbors:
                if n in wall_tiles:
                    return False
            return True

        valid_tiles = [t for t in floor_tiles if is_clear(t)]
        used = set()

        chest_tiles = []
        for tile in SPAWN_CHEST_TILES:
            if tile in valid_tiles and tile not in used:
                chest_tiles.append(tile)
                used.add(tile)

        # если каких-то позиций не хватило, добираем случайными
        while len(chest_tiles) < 3 and valid_tiles:
            tile = random.choice(valid_tiles)
            if tile in used:
                continue
            chest_tiles.append(tile)
            used.add(tile)

        if 'chest' not in self.all_sprites:
            self.all_sprites['chest'] = arcade.SpriteList()

        for tile_x, tile_y in chest_tiles:
            center_x = self.x * CHUNCK_SIZE[0] * TILE_SIZE + TILE_SIZE * (tile_x + 1)
            center_y = self.y * CHUNCK_SIZE[1] * TILE_SIZE + TILE_SIZE * (tile_y + 1)
            self.all_sprites['chest'].append(Chest(center_x=center_x, center_y=center_y))

    def load_sprites_from_data(self, data: dict) -> dict:
        # Все спрайты с комнат
        sprites = {
            'floor': arcade.SpriteList(),
            'wall': arcade.SpriteList(),
            'interactive': arcade.SpriteList()
        }

        for object_type in data:
            for j, i in data[object_type]:
                tile_x = self.x * CHUNCK_SIZE[0] * TILE_SIZE + TILE_SIZE * (j + 1)
                tile_y = self.y * CHUNCK_SIZE[1] * TILE_SIZE + TILE_SIZE * (i + 1)

                # Пол
                if object_type == '1':
                    sprites['floor'].append(Floor(
                        None, 1, tile_x, tile_y
                    ))

                #  Стена
                if object_type == '2':
                    sprites['wall'].append(Wall(
                        None, 1, tile_x, tile_y
                    ))
                
                if object_type == '3':
                    sprites['interactive'].append(InetactiveObject(
                        None, 1, tile_x, tile_y
                    ))

        return sprites
